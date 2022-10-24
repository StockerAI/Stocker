from sqlalchemy import Column, Integer, String, UniqueConstraint
from Model.base import Base

class Tickers(Base):
    __tablename__ = 'Tickers'

    tickerId = Column(Integer, primary_key=True)
    stockMarket = Column(String, nullable=False)
    tickerName = Column(String, nullable=False)
    organizationName = Column(String)

    UniqueConstraint(stockMarket, tickerName)

    def __repr__(self):
        return f"Tickers(tickerId={self.tickerId!r}, stockMarket={self.stockMarket} tickerName={self.tickerName!r}, organizationName={self.organizationName!r})"
