from Model.Engine_Creator import Engine_Creator
from sqlalchemy import create_engine
from Model.Tickers import Base

if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://postgres:123456789plaka@localhost/StockerDB", echo=True)
    with engine.connect() as connection:
        with connection.begin():
            Base.metadata.create_all(engine)

    # with Engine_Creator() as ec:
        # engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")
        # print('awd')