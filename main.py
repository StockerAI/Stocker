from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries, stocks
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Base_Parsers.SQL_Select_To_Generator_Parsers.sql_select_to_generators_parser import sql_select_to_generator
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser

if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://' + config()['user'] + ':' + config()['password'] + '@' + config()['host'] + '/' + config()['database'] + '', echo=True)    
    with engine.connect() as connection:
        # with connection.begin():
        with Session(engine).begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

        with Session(engine).begin():
            base_inserter(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__], values=ticker_value_list)
            # base.Base.metadata.tables[tickers.Tickers.__tablename__].drop(engine)

        with Session(engine).begin():
            base_inserter(connection=connection, table=base.Base.metadata.tables[stocks.Stocks.__tablename__], values=stock_parser(sql_select_to_generator(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))))
            # stock_parser(sql_select_to_generator(base_selector(connection=connection, table=base.Base.metadata.tables[tickers.Tickers.__tablename__]))).to_sql(base.Base.metadata.tables[stocks.Stocks.__tablename__], engine, if_exists='append')
            # base.Base.metadata.tables[stocks.Stocks.__tablename__].drop(engine)

        # Uncomment bellow line to drop everything on the database.
        # base.Base.metadata.drop_all(engine, checkfirst=True)