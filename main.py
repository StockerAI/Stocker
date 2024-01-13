import os
import numpy
import pandas
import datetime
from tqdm import tqdm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from Model import base, tickers, stocks, company_details
from Model.config import config
from Base_Parsers.company_details_parsers.company_details_parser import company_details_parser
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser
from Base_Parsers.SQL_Select_To_Data_Parsers.sql_select_to_data_parser import sql_select_to_list
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Control.Util_Controllers.modin_utils import init_modin
from Control.Util_Controllers.option_utils import get_args
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Updaters.base_conditional_updater import base_conditional_updater
from Control.Base_Controllers.Selectors.base_count_selector import base_count_selector
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Control.Base_Controllers.Selectors.base_column_selector import base_column_selector
from Control.Base_Controllers.Selectors.base_distinct_column_selector import base_distinct_column_selector
from Control.Base_Controllers.Selectors.base_conditional_in_selector import base_conditional_in_selector
from Control.Base_Controllers.Selectors.base_conditional_ordered_limited_selector import base_conditional_ordered_limited_selector
from Control.Executioner.silent_executioner import silent_executioner
from Control.Loggers.base_logger import Logger

def initialize_database(engine):
    """
    Initializes the database by creating all tables if they don't exist.
    Optionally, it can drop all tables before creating them.
    """
    with Session(engine) as session:
        with session.begin():
            base.Base.metadata.create_all(engine, checkfirst=True)
            # Uncomment the next line to drop everything in the database.
            # base.Base.metadata.drop_all(engine, checkfirst=True)

def insert_tickers_if_not_exists(engine, connection):
    """
    Inserts tickers into the database if they don't exist.
    """
    with Session(engine) as session:
        with session.begin():
            tickers_table = base.Base.metadata.tables[tickers.Tickers.__tablename__]
            result = silent_executioner(connection, base_count_selector(tickers_table)).fetchone()

            if not result or result[0] == 0:
                silent_executioner(connection, base_inserter(tickers_table, ticker_value_list))
        # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)

def insert_stocks_if_not_exists(engine, connection):
    """
    Inserts stocks into the database if they don't exist.
    """
    with Session(engine).begin():
        stocks_table = base.Base.metadata.tables[stocks.Stocks.__tablename__]
        tickers_table = base.Base.metadata.tables[tickers.Tickers.__tablename__]

        # Check if stocks need to be inserted
        result = silent_executioner(connection, base_count_selector(stocks_table)).fetchone()
        if not result or result[0] == 0:
            # Insert logic when there are no stocks in the table
            tickers_list = sql_select_to_list(silent_executioner(connection, base_selector(tickers_table)))
            for ticker in tqdm(tickers_list, desc="Parsing Stock Data", unit="ticker", total=len(tickers_list)):
                silent_executioner(connection, base_inserter(stocks_table, stock_parser(ticker=ticker)))
        else:
            # Logic to handle when some stocks are already present
            tickers_ticker_id_list = pandas.read_sql(base_column_selector(tickers_table.c.tickerId, tickers_table), connection).squeeze().tolist()
            stocks_ticker_id_list = pandas.read_sql(base_distinct_column_selector(stocks_table.c.tickerId, stocks_table), connection).squeeze().tolist()
            id_differences = numpy.setdiff1d(tickers_ticker_id_list, stocks_ticker_id_list)

            if id_differences.tolist():
                tickers_list = sql_select_to_list(silent_executioner(connection, base_conditional_in_selector(tickers_table, tickers_table.c.tickerId, id_differences.tolist())))
                for ticker in tqdm(tickers_list, desc="Parsing Stock Data", unit="ticker", total=len(tickers_list)):
                    silent_executioner(connection, base_inserter(stocks_table, stock_parser(ticker=ticker)))

        # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)

def insert_new_stock_values_based_on_date(engine, connection, logger):
    """
    Inserts new stock values into the database based on date.
    """
    with Session(engine).begin():
        stocks_table = base.Base.metadata.tables[stocks.Stocks.__tablename__]
        tickers_table = base.Base.metadata.tables[tickers.Tickers.__tablename__]

        # Check if there are existing stocks in the table
        result = silent_executioner(connection, base_count_selector(stocks_table)).fetchone()
        if result and result[0] > 0:
            tickers_list = sql_select_to_list(silent_executioner(connection, base_selector(tickers_table)))
            for ticker in tqdm(tickers_list, desc="Parsing Stock Data", unit="ticker", total=len(tickers_list)):
                try:
                    last_stock_value_date_ping = sql_select_to_list(
                        silent_executioner(
                            connection=connection,
                            SIUD=base_conditional_ordered_limited_selector(
                                table=stocks_table,
                                columnName=stocks_table.c.tickerId,
                                columnValue=ticker[0],
                                orderColumn=stocks_table.c.date,
                                limitNumber=1,
                                descending=True
                            ),
                        )
                    )[0][2] + datetime.timedelta(days=1)

                    silent_executioner(
                        connection=connection,
                        SIUD=base_inserter(
                            table=stocks_table,
                            values=stock_parser(ticker=ticker, start_date=last_stock_value_date_ping),
                        ),
                    )
                except Exception as e:
                    logger.info(f"Something went wrong with smart insertion in {stocks_table} for ticker {ticker[0]}: {e}")

        # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)

def insert_company_details_if_not_exists(engine, connection, logger):
    """
    Inserts company details into the database if they don't exist.
    """
    with Session(engine).begin():
        company_details_table = base.Base.metadata.tables[company_details.Company_Details.__tablename__]
        tickers_table = base.Base.metadata.tables[tickers.Tickers.__tablename__]

        # Check if company details need to be inserted
        result = silent_executioner(connection, base_count_selector(company_details_table)).fetchone()
        if not result or result[0] == 0:
            # Insert logic when there are no company details in the table
            tickers_list = sql_select_to_list(silent_executioner(connection, base_selector(tickers_table)))
            for ticker in tqdm(tickers_list, desc="Parsing Company Details Data", unit="ticker", total=len(tickers_list)):
                silent_executioner(connection, base_inserter(company_details_table, [company_details_parser(ticker=ticker)]))
        else:
            # Logic to handle when some company details are already present
            tickers_ticker_id_list = pandas.read_sql(base_column_selector(tickers_table.c.tickerId, tickers_table), connection).squeeze().tolist()
            company_details_ticker_id_list = pandas.read_sql(base_distinct_column_selector(company_details_table.c.tickerId, company_details_table), connection).squeeze().tolist()
            id_differences = numpy.setdiff1d(tickers_ticker_id_list, company_details_ticker_id_list)

            if id_differences.tolist():
                tickers_list = sql_select_to_list(silent_executioner(connection, base_conditional_in_selector(tickers_table, tickers_table.c.tickerId, id_differences.tolist())))
                for ticker in tqdm(tickers_list, desc="Parsing Company Details Data", unit="ticker", total=len(tickers_list)):
                    try:
                        silent_executioner(connection, base_inserter(company_details_table, [company_details_parser(ticker=ticker)]))
                    except Exception as e:
                        logger.info(f"Something went wrong with smart insertion in {company_details_table} for ticker {ticker[0]}: {e}")

        # base.Base.metadata.tables[company_details.Company_Details.__tablename__].drop(engine)

def update_company_details(engine, connection, logger):
    """
    Update company details into the database.
    """
    with Session(engine).begin():
        company_details_table = base.Base.metadata.tables[company_details.Company_Details.__tablename__]
        tickers_table = base.Base.metadata.tables[tickers.Tickers.__tablename__]

        tickers_list = sql_select_to_list(silent_executioner(connection, base_selector(tickers_table)))

        for ticker in tqdm(tickers_list, desc="Parsing Company Details Data", unit="ticker", total=len(tickers_list)):
            try:
                silent_executioner(connection, base_conditional_updater(company_details_table, company_details_table.c.tickerId, ticker[0], company_details_parser(ticker=ticker)))
            except Exception as e:
                logger.info(f"Something went wrong with smart insertion in {company_details_table} for ticker {ticker[0]}: {e}")

def main():
    os.environ["MODIN_ENGINE"] = "ray"  # Use Ray as the backend for Modin
    # Assuming init_modin is a function that initializes Modin with Ray
    init_modin()

    # Database configuration
    db_config = config()
    db_url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(db_url, echo=False)

    # Argument parsing and Logger setup
    args = get_args()
    logger = Logger(
        "Logger",
        log_file=args.log_file,
        verbose=args.verbose,
        out_dir=args.log_dir,
        enable_datetime_stamp=args.enable_datetime_stamp
    )

    # Database operations
    with engine.connect() as connection:
        initialize_database(engine)
        insert_tickers_if_not_exists(engine, connection)
        insert_stocks_if_not_exists(engine, connection)
        insert_new_stock_values_based_on_date(engine, connection, logger)
        insert_company_details_if_not_exists(engine, connection, logger)
        update_company_details(engine, connection, logger)

if __name__ == "__main__":
    main()
