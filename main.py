from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries, stocks, company_details
from Control.Executioner.base_executioner import base_executioner
from Control.Executioner.silent_executioner import silent_executioner
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Control.Base_Controllers.Selectors.base_column_selector import base_column_selector
from Control.Base_Controllers.Selectors.base_distinct_column_selector import (
    base_distinct_column_selector,
)
from Control.Base_Controllers.Selectors.base_count_selector import base_count_selector
from Control.Base_Controllers.Selectors.base_conditional_in_selector import (
    base_conditional_in_selector,
)
from Control.Base_Controllers.Selectors.base_conditional_ordered_limited_selector import (
    base_conditional_ordered_limited_selector,
)
from Control.Base_Controllers.Updaters.base_updater import base_updater
from Control.Base_Controllers.Updaters.base_conditional_updater import (
    base_conditional_updater,
)
from Base_Parsers.SQL_Select_To_Data_Parsers.sql_select_to_data_parser import (
    sql_select_to_generator,
    sql_select_to_list,
)
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser
from Base_Parsers.company_details_parsers.company_details_parser import (
    company_details_parser,
)
from Control.Loggers.base_logger import Logger
from Control.Util_Controllers.option_utils import get_args
from Control.Util_Controllers.modin_utils import init_modin
from tqdm import tqdm
import os
import datetime
import pandas
import numpy


if __name__ == "__main__":
    os.environ["MODIN_ENGINE"] = "ray"  # Modin will use Ray
    init_modin()
    engine = create_engine(
        "postgresql+psycopg2://"
        + config()["user"]
        + ":"
        + config()["password"]
        + "@"
        + config()["host"]
        + "/"
        + config()["database"]
        + "",
        echo=False,
    )
    args = get_args()
    # NOTE: name of logger must be static, otherwise it 
    # will create a new logger every time.
    logger = Logger(
        "Logger",
        log_file=args.log_file,
        verbose=args.verbose,
        out_dir=args.log_dir,
        enable_datetime_stamp=args.enable_datetime_stamp
    )
    with engine.connect() as connection:
        # with connection.begin():
        with Session(engine).begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

        # region Inserter for Tickers table.
        with Session(engine).begin():
            if not sql_select_to_list(
                silent_executioner(
                    connection=connection,
                    SIUD=base_count_selector(
                        table=base.Base.metadata.tables[tickers.Tickers.__tablename__]
                    ),
                )
            )[0]._data[0]:
                from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list

                silent_executioner(
                    connection=connection,
                    SIUD=base_inserter(
                        table=base.Base.metadata.tables[tickers.Tickers.__tablename__],
                        values=ticker_value_list,
                    ),
                )
            # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)
        # endregion

        # region Inserter for Stocks table.
        with Session(engine).begin():
            if not sql_select_to_list(
                silent_executioner(
                    connection=connection,
                    SIUD=base_count_selector(
                        table=base.Base.metadata.tables[stocks.Stocks.__tablename__]
                    ),
                )
            )[0]._data[0]:
                tickers_list = sql_select_to_list(
                    silent_executioner(
                        connection=connection,
                        SIUD=base_selector(
                            table=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ]
                        ),
                    )
                )
                for ticker in tqdm(
                    tickers_list,
                    desc="Parsing Stock Data",
                    unit="ticker",
                    total=len(tickers_list),
                ):
                    silent_executioner(
                        connection=connection,
                        SIUD=base_inserter(
                            table=base.Base.metadata.tables[
                                stocks.Stocks.__tablename__
                            ],
                            values=stock_parser(ticker=ticker),
                        ),
                    )
            else:
                tickers_ticker_id_list = (
                    pandas.read_sql(
                        base_column_selector(
                            columnName=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ].c.tickerId,
                            table=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ],
                        ),
                        connection,
                    )
                    .squeeze()
                    .tolist()
                )
                stocks_ticker_id_list = (
                    pandas.read_sql(
                        base_distinct_column_selector(
                            columnName=base.Base.metadata.tables[
                                stocks.Stocks.__tablename__
                            ].c.tickerId,
                            table=base.Base.metadata.tables[
                                stocks.Stocks.__tablename__
                            ],
                        ),
                        connection,
                    )
                    .squeeze()
                    .tolist()
                )
                id_differences = numpy.setdiff1d(
                    tickers_ticker_id_list, stocks_ticker_id_list
                )
                if id_differences.tolist():
                    tickers_list = sql_select_to_list(
                        silent_executioner(
                            connection=connection,
                            SIUD=base_conditional_in_selector(
                                table=base.Base.metadata.tables[
                                    tickers.Tickers.__tablename__
                                ],
                                columnName=base.Base.metadata.tables[
                                    tickers.Tickers.__tablename__
                                ].c.tickerId,
                                columnValues=id_differences.tolist(),
                            ),
                        )
                    )
                    for ticker in tqdm(
                        tickers_list,
                        desc="Parsing Stock Data",
                        unit="ticker",
                        total=len(tickers_list),
                    ):
                        silent_executioner(
                            connection=connection,
                            SIUD=base_inserter(
                                table=base.Base.metadata.tables[
                                    stocks.Stocks.__tablename__
                                ],
                                values=stock_parser(ticker=ticker),
                            ),
                        )
            # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)
        # endregion

        # region Inserter for Stocks table, new stock vales based on date.
        with Session(engine).begin():
            if sql_select_to_list(
                silent_executioner(
                    connection=connection,
                    SIUD=base_count_selector(
                        table=base.Base.metadata.tables[stocks.Stocks.__tablename__]
                    ),
                )
            )[0]._data[0]:
                tickers_list = sql_select_to_list(
                    silent_executioner(
                        connection=connection,
                        SIUD=base_selector(
                            table=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ]
                        ),
                    )
                )
                for ticker in tqdm(
                    tickers_list,
                    desc="Parsing Stock Data",
                    unit="ticker",
                    total=len(tickers_list),
                ):
                    try:
                        last_stock_value_date_ping = sql_select_to_list(
                            silent_executioner(
                                connection=connection,
                                SIUD=base_conditional_ordered_limited_selector(
                                    table=base.Base.metadata.tables[
                                        stocks.Stocks.__tablename__
                                    ],
                                    columnName=base.Base.metadata.tables[
                                        stocks.Stocks.__tablename__
                                    ].c.tickerId,
                                    columnValue=ticker[0],
                                    orderColumn=base.Base.metadata.tables[
                                        stocks.Stocks.__tablename__
                                    ].c.date,
                                    limitNumber=1,
                                ),
                            )
                        )[0][2] + datetime.timedelta(days=1)
                        silent_executioner(
                            connection=connection,
                            SIUD=base_inserter(
                                table=base.Base.metadata.tables[
                                    stocks.Stocks.__tablename__
                                ],
                                values=stock_parser(
                                    ticker=ticker, start_date=last_stock_value_date_ping
                                ),
                            ),
                        )
                    except:
                        logger.info("Something went wrong with smart insertion.")
        # endregion

        # region Inserter for CompanyDetails table.
        with Session(engine).begin():
            if not sql_select_to_list(
                silent_executioner(
                    connection=connection,
                    SIUD=base_count_selector(
                        table=base.Base.metadata.tables[
                            company_details.Company_Details.__tablename__
                        ]
                    ),
                )
            )[0]._data[0]:
                tickers_list = sql_select_to_list(
                    silent_executioner(
                        connection=connection,
                        SIUD=base_selector(
                            table=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ]
                        ),
                    )
                )
                for ticker in tqdm(
                    tickers_list,
                    desc="Parsing Company Details Data",
                    unit="ticker",
                    total=len(tickers_list),
                ):

                    silent_executioner(
                        connection=connection,
                        SIUD=base_inserter(
                            table=base.Base.metadata.tables[
                                company_details.Company_Details.__tablename__
                            ],
                            values=[company_details_parser(ticker=ticker)],
                        ),
                    )
            else:
                tickers_ticker_id_list = (
                    pandas.read_sql(
                        base_column_selector(
                            columnName=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ].c.tickerId,
                            table=base.Base.metadata.tables[
                                tickers.Tickers.__tablename__
                            ],
                        ),
                        connection,
                    )
                    .squeeze()
                    .tolist()
                )
                company_details_ticker_id_list = (
                    pandas.read_sql(
                        base_distinct_column_selector(
                            columnName=base.Base.metadata.tables[
                                company_details.Company_Details.__tablename__
                            ].c.tickerId,
                            table=base.Base.metadata.tables[
                                company_details.Company_Details.__tablename__
                            ],
                        ),
                        connection,
                    )
                    .squeeze()
                    .tolist()
                )
                id_differences = numpy.setdiff1d(
                    tickers_ticker_id_list, company_details_ticker_id_list
                )
                if id_differences.tolist():
                    tickers_list = sql_select_to_list(
                        silent_executioner(
                            connection=connection,
                            SIUD=base_conditional_in_selector(
                                table=base.Base.metadata.tables[
                                    tickers.Tickers.__tablename__
                                ],
                                columnName=base.Base.metadata.tables[
                                    tickers.Tickers.__tablename__
                                ].c.tickerId,
                                columnValues=id_differences.tolist(),
                            ),
                        )
                    )
                    for ticker in tqdm(
                        tickers_list,
                        desc="Parsing Company Details Data",
                        unit="ticker",
                        total=len(tickers_list),
                    ):
                        silent_executioner(
                            connection=connection,
                            SIUD=base_inserter(
                                table=base.Base.metadata.tables[
                                    company_details.Company_Details.__tablename__
                                ],
                                values=stock_parser(ticker=ticker),
                            ),
                        )
            # base.Base.metadata.tables[company_details.Company_Details.__tablename__].drop(engine)
        # endregion

        # Uncomment bellow line to drop everything on the database.
        # base.Base.metadata.drop_all(engine, checkfirst=True)
