from sqlalchemy import create_engine
from Model.config import config
from Model import base

from Model import Tickers, Countries

if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://" + config()['user'] + ":" + config()['password'] + "@" + config()['host'] + "/" + config()['database'] + "", echo=True)    
    with engine.connect() as connection:
        with connection.begin():
            base.Base.metadata.create_all(engine, checkfirst=True)

            ticker_creator = Tickers.Tickers()
            countries_creator = Countries.Countries()