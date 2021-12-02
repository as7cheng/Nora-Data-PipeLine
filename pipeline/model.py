"""
File to declare data models and schemas
"""
from sqlalchemy import Column
from sqlalchemy.types import ARRAY, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class Business(BASE):
    """
    Class of business data entries
    """
    __tablename__ = 'business'

    # Business schema
    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    image = Column(Text)
    url = Column(Text)
    tags = Column(ARRAY(Text))
    rating = Column(Numeric)
    transaction = Column(ARRAY(Text))
    price = Column(Text)
    addr = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip_code = Column(Text)
    phone = Column(Text)
    timestamp = Column(Text)
    metropolitan = Column(Text)
    term = Column(Text)
    city_population = Column(Numeric)
