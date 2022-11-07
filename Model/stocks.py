from sqlalchemy import BigInteger, Column, Date, Float, Integer, String, UniqueConstraint
from Model.base import Base

class Stocks(Base):
    '''
    Stocks table class creation.

    Columns:
        `stockId`: The ID of the Stock,
        `tickerId`: The ID of the Ticker,
        `date`: The date value retrieved from the `yahoo_fin` API,
        `open`: The open value retrieved from the `yahoo_fin` API,
        `high`: The high value retrieved from the `yahoo_fin` API,
        `low`: The low value retrieved from the `yahoo_fin` API,
        `close`: The close value retrieved from the `yahoo_fin` API,
        `adjclose`: The adjusted close value retrieved from the `yahoo_fin` API,
        `volume`: The volume value retrieved from the `yahoo_fin` API.
    '''

    __tablename__ = 'Stocks'
    '''
    The name of the table that will be registered on the Database.
    '''

    stockId = Column(Integer, primary_key=True, nullable=False)
    tickerId = Column(Integer, nullable=False)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjclose = Column(Float)
    volume = Column(Float)

    UniqueConstraint(tickerId, date)

    def __repr__(self):
        return f'Stocks(stockId={self.stockId!r}, tickerId={self.tickerId!r} date={self.date!r}, open={self.open!r}, high={self.high!r}, low={self.low!r}, close={self.close!r}, adjclose={self.adjclose!r}, volume={self.volume!r})'
