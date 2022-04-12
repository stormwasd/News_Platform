import scrapy


class GraspShumacnSpider(scrapy.Spider):
    name = 'grasp_shumacn'
    allowed_domains = ['www.shumacn.com']
    start_urls = ['http://www.shumacn.com/']

    def parse(self, response):
        pass
