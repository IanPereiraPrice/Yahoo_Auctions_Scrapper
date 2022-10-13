from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings
import os 
from dotenv import load_dotenv



#Get DB username/password
load_dotenv()
drivername="postgresql"
user= os.getenv('username_db')
passwd= os.getenv('password')
host= "localhost"
port= os.getenv('hostname')
db_name= os.getenv('dbname')


#CONNECTION_STRING = f'{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?client_encoding=utf8'

CONNECTION_STRING = 'postgresql://postgres:Phs2015@localhost:5432/Yugioh'


Base = declarative_base()



def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # return create_engine(get_project_settings().get("CONNECTION_STRING"))
   
    return create_engine(CONNECTION_STRING)


def create_table(engine):
    Base.metadata.create_all(engine)


# card_sales_staging = Table('Card_Sales_Staging', Base.metadata,
#     # id = Column('id',Integer, primary_key=True),
#     auction_id = Column('auction_id', String(15),unique=True),
    # title = Column('title', Text()),
    # price = Column('price', String(15)),
    # bids = Column('bids', Integer),
    # tax = Column('tax', String(10)),
    # auction_start = Column('auction_start', String(25)),
    # auction_end = Column('auction_end', String(25)),
    # auction_extension = Column('auction_extension', String(10)),
    # best_offer_accepted = Column('best_offer_accepted', String(10)),
    # all_images = Column('all_images', Text())

# )



# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
# class Card_Sales_Staging(Base):



class Sold_Listings_Holding(Base):
    __tablename__ = "Card_Sales_Staging"
    # __tablename__ = 'sold_listings_holding'

    id = Column(Integer, primary_key=True)
    auction_id = Column('auction_id', String(15),unique=True)
    title = Column('title', String(1000),nullable=False)
    price = Column('price', String(15))
    bids = Column('bids', Integer)
    tax = Column('tax', String(25))
    auction_start = Column('auction_start', String(25))
    auction_end = Column('auction_end', String(25))
    auction_extension = Column('auction_extension', String(14))
    best_offer_accepted = Column('best_offer_accepted', String(13))
    all_images = Column('all_images', String(10000),nullable=False)