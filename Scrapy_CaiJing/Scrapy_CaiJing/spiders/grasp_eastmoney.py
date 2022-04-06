import scrapy
from Scrapy_test.items import ScrapyTestItem
from scrapy.utils import request
from datetime import datetime


class GraspEastmoneySpider(scrapy.Spider):
    name = 'grasp_eastmoney'
    allowed_domains = ['finance.eastmoney.com']
    start_urls = ['http://finance.eastmoney.com/']

    def parse(self, response):
        pass
