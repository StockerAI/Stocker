from Model.config import config
from Model.Tickers import Base
from sqlalchemy import create_engine

if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://" + config()['user'] + ":" + config()['password'] + "@" + config()['host'] + "/" + config()['database'] + "", echo=True)    
    with engine.connect() as connection:
        with connection.begin():
            Base.metadata.create_all(engine)
