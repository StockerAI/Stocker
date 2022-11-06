from sqlalchemy import Column, Integer, String
from Model.base import Base

class Countries(Base):
    '''
    Countries table class creation.

    Columns:
        `countryId`: The ID of the Country,
        `countryName`: The Name of the Country.
    '''

    __tablename__ = 'Countries'
    '''
    The name of the table that will be registered on the Database.
    '''

    countryId = Column(Integer, primary_key=True)
    countryName = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'Countries(countryId={self.countryId!r}, countryName={self.countryName!r})'
