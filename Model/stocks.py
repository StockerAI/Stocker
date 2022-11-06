from sqlalchemy import BigInteger, Column, Date, Float, Integer, String, UniqueConstraint
from Model.base import Base

class Stocks(Base):
    __tablename__ = 'Stocks'

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
