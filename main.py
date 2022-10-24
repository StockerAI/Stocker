from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list

if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://" + config()['user'] + ":" + config()['password'] + "@" + config()['host'] + "/" + config()['database'] + "", echo=True)    
    with engine.connect() as connection:
        # with connection.begin():
        with Session(engine).begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

        with Session(engine).begin():
            base_inserter(connection=connection, table=base.Base.metadata.tables['Tickers'], values=ticker_value_list)

        with Session(engine).begin():
            base_selector(connection=connection, table=base.Base.metadata.tables['Tickers'])

        # Uncomment bellow line to drop everything on the database.
        # base.Base.metadata.drop_all(engine, checkfirst=True)