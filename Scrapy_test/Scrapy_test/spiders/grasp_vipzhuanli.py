import scrapy
from Scrapy_test.items import ScrapyTestItem
from scrapy.utils import request
from datetime import datetime


class GraspVipzhuanliSpider(scrapy.Spider):
    name = 'grasp_vipzhuanli'
    allowed_domains = ['www.vipzhuanli.com']
    start_urls = ['http://www.vipzhuanli.com/']

    def start_requests(self):
        for i in range(2, 3):
            url = f'https://www.vipzhuanli.com/patent/list.html?kw=%u516C%u8DEF%u8FD0%u8F93&page={i}'
            'https://www.vipzhuanli.com/patent/list.html?kw=%u516C%u8DEF%u8FD0%u8F93&page=2'
            req = scrapy.Request(url, callback=self.parse, dont_filter=True)
            yield req

    def parse(self, response):
        detail_url_list = response.xpath(
            "//li[@class='s-con-t']/a[@class='px16']/@href").extract()
        title_list = response.xpath(
            "//li[@class='s-con-t']/a[@class='px16']/text()").extract()
        zhuanli_list = response.xpath(
            "//li[@class='s-con-t']/a[2]/text()").extract()
        for i in range(len(detail_url_list)):
            url = detail_url_list[i]
            req = scrapy.Request(
                url='https://www.vipzhuanli.com' + url,
                callback=self.parse_detail,
                dont_filter=True)
            news_id = request.request_fingerprint(req)
            title = title_list[i]
            zhuanli = zhuanli_list[i]
            req.meta.update({'news_id': news_id})
            req.meta.update({'title': title})
            req.meta.update({'zhuanli': zhuanli})
            yield req

    def parse_detail(self, response):
        zhuanli = response.meta['zhuanli']
        title = response.meta['title']
        news_id = response.meta['news_id']
        content = ''.join(response.xpath(
            "//div[@class='con-box']").extract())

        item = ScrapyTestItem()
        item['news_id'] = news_id
        item['category'] = '交通物流'
        item['content_url'] = response.url
        item['title'] = title
        item['issue_time'] = datetime.now().strftime(
            '%Y-%m-%d')
        item['title_image'] = None
        item['information_source'] = '钻瓜专利网'
        item['content'] = content
        item['author'] = None
        item['update_time'] = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        item['cleaning_status'] = 0
        item['images'] = None
        item['source'] = None
        self.logger.info(item)
        yield item


if __name__ == '__main__':
    import scrapy.cmdline as cmd
    cmd.execute(['scrapy', 'crawl', 'grasp_vipzhuanli'])