from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries, stocks, company_details
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Control.Base_Controllers.Selectors.base_conditional_ordered_limited_selector import base_conditional_ordered_limited_selector
from Control.Base_Controllers.Updaters.base_updater import base_updater
from Control.Base_Controllers.Updaters.base_conditional_updater import base_conditional_updater
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Base_Parsers.SQL_Select_To_Data_Parsers.sql_select_to_data_parser import sql_select_to_generator, sql_select_to_list
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser
from Base_Parsers.company_details_parsers.company_details_parser import company_details_parser
from Control.Util_Controllers.modin_utils import init_modin
from tqdm import tqdm
import yfinance
import os
import datetime


if __name__ == '__main__':
    os.environ["MODIN_ENGINE"] = "ray" # Modin will use Ray
    init_modin()
    engine = create_engine('postgresql+psycopg2://' + config()['user'] + ':' + config()['password'] + '@' + config()['host'] + '/' + config()['database'] + '', echo=False)    
    with engine.connect() as connection:
        # with connection.begin():
        with Session(engine).begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

        # region Inserter for Tickers table.
        with Session(engine).begin():
            if not base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]).rowcount:
                base_inserter(
                    connection=connection,
                    table=base.Base.metadata.tables[tickers.Tickers.__tablename__],
                    values=ticker_value_list)
            # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)
        # endregion

        # region Updater for Tickers table.
        # with Session(engine).begin():
        #     tickerList = sql_select_to_list(base_selector(
        #         connection=connection,
        #         table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))
        #     for ticker in tqdm(tickerList, desc='Parsing Stock Data', unit=' ticker', total=len(tickerList)):
        #         try:
        #             base_conditional_updater(
        #                 connection=connection,
        #                 table=base.Base.metadata.tables[tickers.Tickers.__tablename__],
        #                 columnName=base.Base.metadata.tables[tickers.Tickers.__tablename__].c.tickerId,
        #                 columnValue=ticker[0],
        #                 values=[{base.Base.metadata.tables[tickers.Tickers.__tablename__].c.organizationName.name: yfinance.Ticker(ticker[2]).info['longName']}])
        #         except:
        #             base_conditional_updater(
        #                 connection=connection,
        #                 table=base.Base.metadata.tables[tickers.Tickers.__tablename__],
        #                 columnName=base.Base.metadata.tables[tickers.Tickers.__tablename__].c.tickerId,
        #                 columnValue=ticker[0],
        #                 values=[{base.Base.metadata.tables[tickers.Tickers.__tablename__].c.organizationName.name: None}])
        #     # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)
        # endregion

        # region Inserter for Stocks table.
        with Session(engine).begin():
            if not base_selector(connection=connection, table=base.Base.metadata.tables[stocks.Stocks.__tablename__]).rowcount:
                tickers = sql_select_to_list(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))
                for ticker in tqdm(tickers, desc='Parsing Stock Data', unit=' ticker', total=len(tickers)):
                    base_inserter(
                        connection=connection,
                        table=base.Base.metadata.tables[stocks.Stocks.__tablename__],
                        values=stock_parser(ticker=ticker))
            # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)
        # endregion

        # region Inserter for CompanyDetails table.
        with Session(engine).begin():
            if not base_selector(connection=connection, table=base.Base.metadata.tables[company_details.Company_Details.__tablename__]).rowcount:
                tickers = sql_select_to_list(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))
                for ticker in tqdm(tickers, desc='Parsing Stock Data', unit=' ticker', total=len(tickers)):
                    base_inserter(
                        connection=connection,
                        table=base.Base.metadata.tables[company_details.Company_Details.__tablename__],
                        values=[company_details_parser(ticker=ticker)])
            # base.Base.metadata.tables[company_details.Company_Details.__tablename__].drop(engine)
        # endregion

        # region Inserter for Stocks table, new stock vales based on date.
        with Session(engine).begin():
            if base_selector(connection=connection, table=base.Base.metadata.tables[stocks.Stocks.__tablename__]).rowcount:
                tickers = sql_select_to_list(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))
                for ticker in tqdm(tickers, desc='Parsing Stock Data', unit=' ticker', total=len(tickers)):
                    try:
                        last_stock_value_date_ping = sql_select_to_list(
                                base_conditional_ordered_limited_selector(
                                    connection=connection,
                                    table=base.Base.metadata.tables[stocks.Stocks.__tablename__],
                                    columnName=base.Base.metadata.tables[stocks.Stocks.__tablename__].c.tickerId,
                                    columnValue=ticker[0],
                                    orderColumn=base.Base.metadata.tables[stocks.Stocks.__tablename__].c.date,
                                    limitNumber=1
                                )
                            )[0][2] + datetime.timedelta(days=1)
                        base_inserter(
                            connection=connection,
                            table=base.Base.metadata.tables[stocks.Stocks.__tablename__],
                            values=stock_parser(ticker=ticker, start_date=last_stock_value_date_ping))
                    except:
                        pass
                        # print('Something went wrong with smart insertion.') # TODO: This must be a logger.
        # endregion

        # Uncomment bellow line to drop everything on the database.
        # base.Base.metadata.drop_all(engine, checkfirst=True)
