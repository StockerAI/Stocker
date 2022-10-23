from sqlalchemy import Column, Integer, String
from Model.base import Base

class Countries(Base):
    __tablename__ = 'Countries'

    countryId = Column(Integer, primary_key=True)
    countryName = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"Countries(countryId={self.countryId!r}, countryName={self.countryName!r})"
