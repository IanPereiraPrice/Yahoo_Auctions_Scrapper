# Define your item pipelines here
import sys
import os 
from dotenv import load_dotenv

from sqlalchemy.orm import sessionmaker


import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'E:\Ian\Ebay_Project\card_scraper\card_scraper')

from models import db_connect, create_table, Sold_Listings_Holding
# from card_scraper.models import db_connect, create_table,sold_listings_holding
import logging


# Host_Name = os.getenv('hostname')
# User_Name= os.getenv('username')
# Password= os.getenv('password')
# Database_Name= os.getenv('dbname')

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


#Connection to db




class Yahoo_Listings_Pipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        
        session = self.Session()
        sold_listings_holding = Sold_Listings_Holding()
        
            
    
        sold_listings_holding.auction_id = item['auction_id'],
        sold_listings_holding.title = item['title'],
        sold_listings_holding.price = item['price'],
        sold_listings_holding.bids = item['bids'],
        sold_listings_holding.tax = item['tax'],
        sold_listings_holding.auction_start = item['auction_start'],
        sold_listings_holding.auction_end = item['auction_end'],
        sold_listings_holding.auction_extension = item['auction_extension'],
        sold_listings_holding.best_offer_accepted = item['best_offer_accepted'],
        sold_listings_holding.all_images = item['image_list']
        
        try:
            session.add(sold_listings_holding)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item 
    
    
    
    
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter




from scrapy.exceptions import DropItem
           
           
class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****DuplicatesPipeline: database connected****")

    def process_item(self, item, spider):
        
        #Since result page is sorted by newest, once dupe_id scrape is up tp date
        session = self.Session()
        exist_id = session.query(Sold_Listings_Holding).filter_by(auction_id = item['auction_id']).first()
        session.close()
        #Validate that Auction Id is new else end scrape
        if exist_id is not None:  
            
            raise DropItem("Duplicate item found: %s" % item['auction_id'])
        else:
            return item
            