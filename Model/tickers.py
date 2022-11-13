from sqlalchemy import Column, Integer, String, UniqueConstraint
from Model.base import Base

class Tickers(Base):
    '''
    Tickers table class creation.

    Columns: 
        `tickerId`: The ID of the Ticker,
        `stockMarket`: The Stock Market that the Ticker belongs to,
        `tickerName`: The Name (or Abbreviation) of the Ticker and,
        `organizationName`: The Organization that the Ticker belongs to.
    '''

    __tablename__ = 'Tickers'
    '''
    The name of the table that will be registered on the Database.
    '''

    tickerId = Column(Integer, primary_key=True, nullable=False)
    stockMarket = Column(String, nullable=False)
    tickerName = Column(String, nullable=False)
    organizationName = Column(String)

    UniqueConstraint(stockMarket, tickerName)

    def __repr__(self):
        return f'Tickers(tickerId={self.tickerId!r}, stockMarket={self.stockMarket!r} tickerName={self.tickerName!r}, organizationName={self.organizationName!r})'
