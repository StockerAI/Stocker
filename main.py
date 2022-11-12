from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries, stocks
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Base_Parsers.SQL_Select_To_Generator_Parsers.sql_select_to_data_parser import sql_select_to_generator, sql_select_to_list
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser
from Control.Util_Controllers.modin_utils import init_modin
from tqdm import tqdm


if __name__ == '__main__':
    init_modin()
    engine = create_engine('postgresql+psycopg2://' + config()['user'] + ':' + config()['password'] + '@' + config()['host'] + '/' + config()['database'] + '', echo=True)    
    with engine.connect() as connection:
        # with connection.begin():
        with Session(engine).begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

        with Session(engine).begin():
            base_inserter(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__], values=ticker_value_list)
            # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)

        with Session(engine).begin():
            tickers = sql_select_to_list(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))
            for ticker in tqdm(tickers, desc='Parsing Stock Data', unit=' ticker', total=len(tickers)):
                base_inserter(connection=connection, table=base.Base.metadata.tables[stocks.Stocks.__tablename__], values=stock_parser(ticker=ticker))
            # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)

        # Uncomment bellow line to drop everything on the database.
        # base.Base.metadata.drop_all(engine, checkfirst=True)
