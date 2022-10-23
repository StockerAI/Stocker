from sqlalchemy import create_engine
from Model.config import config
from Model import base
from Model import tickers, countries
from Control.Base_Controllers.Inserters.ticker_inserter import insert_ticker

if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://" + config()['user'] + ":" + config()['password'] + "@" + config()['host'] + "/" + config()['database'] + "", echo=True)    
    with engine.connect() as connection:
        with connection.begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

            ticker_creator = tickers.Tickers()
            countries_creator = countries.Countries()

            insert_ticker(connection=connection)

            # Uncomment bellow line to drop everything on the database.
            # base.Base.metadata.drop_all(engine, checkfirst=True)