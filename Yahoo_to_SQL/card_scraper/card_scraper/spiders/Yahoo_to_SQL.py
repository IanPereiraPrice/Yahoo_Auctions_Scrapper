
import os
import scrapy
from scrapy.utils.project import get_project_settings

from scrapy.crawler import CrawlerRunner
from scrapy.loader import ItemLoader
from twisted.internet import reactor



from scrapy.item import Item

import re

from crochet import setup, wait_for


setup()




translate = {'青眼の白龍':'Blue-Eyes White Dragon',
             'ブルーアイズ・ホワイト・ドラゴン':'Blue-Eyes White Dragon',
             '遊★戯★王':'Yu-Gi-Oh!','ユーギオオー!':'Yu-Gi-Oh!',
             '遊戯王':'Yu-Gi-Oh!'}

class 青眼の白龍_SM_51_sold_spider(scrapy.Spider):
    name = 'BEWD'
    allowed_domains = ['auctions.yahoo.co.jp']
    start_urls =['https://auctions.yahoo.co.jp/closedsearch/closedsearch?va=%E9%9D%92%E7%9C%BC%E3%81%AE%E7%99%BD%E9%BE%8D+sm-51&b=1&n=50&select=6&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=&p=%E9%9D%92%E7%9C%BC%E3%81%AE%E7%99%BD%E9%BE%8D&x=27&y=22']
    custom_settings = {'DOWNLOAD_DELAY':2}
    #scrape urls of items to scrape
    def parse(self,response):
        #location of item page link for all items on page
        all_links = response.xpath('//h3//a/@href').extract()
        for link in all_links:
            yield scrapy.Request(link,callback = self.item_parse)
            # Yields next page of search to scrape
        next_page = response.xpath('//ul[@class="Pager__lists"]//li//a[@data-ylk = "rsec:pagination;slk:next;pos:1"]/@href')
        yield scrapy.Request(next_page,self.parse)
    def item_parse(self,response):
        #Call Item Loader to parse the responses
        l = ItemLoader(item=CardScraperItem(), response=response)
        l.add_xpath('auction_id','//*[@id="l-main"]//div[@class = "l-right"]//li[6]//dd/text()')
        l.add_xpath('title','//*[@id="ProductTitle"]/div/h1//text()')    
        l.add_xpath('price','//*[@id="l-sub"]//dd[@class = "Price__value"]/text()')
        l.add_xpath('bids','//dd[@class = "Count__number"]/text()')
        l.add_xpath('tax','//*[@id="l-sub"]//dd[@class = "Price__value"]/span/text()')
        l.add_xpath('auction_start','//*[@id="l-main"]//div[@class = "l-left"]//li[2]//dd/text()')
        l.add_xpath('auction_end','//*[@id="l-main"]//div[@class = "l-left"]//li[3]//dd/text()')
        l.add_xpath('auction_extension','//*[@id="l-main"]//div[@class = "l-left"]//li[4]//dd/text()')
        l.add_xpath('best_offer_accepted','//*[@id="l-main"]//div[@class = "l-left"]//li[5]//dd/text()')
        l.add_xpath('image_list','//div[contains(@class,"ProductImage__body")]//img/@src')
        return l.load_item()
    
    


from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

# Enable logging for CrawlerRunner

configure_logging()

runner = CrawlerRunner(settings=get_project_settings())

runner.crawl(青眼の白龍_SM_51_sold_spider)