from sqlalchemy import insert
from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Model import base

def insert_ticker(connection):
    TICKERS_TABLE = base.Base.metadata.tables['Tickers']
    connection.execute(insert(TICKERS_TABLE), ticker_value_list)
