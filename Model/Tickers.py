from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from Model.base import Base

class Tickers(Base):
    __tablename__ = 'Tickers'

    tickerId = Column(Integer, primary_key=True)
    tickerName = Column(String, unique=True, nullable=False)
    organizationName = Column(String)

    def __repr__(self):
        return f"Tickers(tickerId={self.tickerId!r}, tickerName={self.tickerName!r}, organizationName={self.organizationName!r})"

