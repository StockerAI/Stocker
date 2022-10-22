from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from Model.base import Base

# Base = Create_Base()

class Countries(Base):
    __tablename__ = 'Countries'

    countryId = Column(Integer, primary_key=True)
    countryName = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Countries(countryId={self.countryId!r}, countryName={self.countryName!r})"