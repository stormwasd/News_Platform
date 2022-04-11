"""
@Description :
@File        : grasp_chinasspp
@Project     : Scrapy_ShiShang
@Time        : 2022/4/11 18:11
@Author      : LiHouJian
@Software    : PyCharm
@issue       :
@change      :
@reason      :
"""


import scrapy
from scrapy.utils import request
from Scrapy_ShiShang.items import ScrapyShishangItem
from Scrapy_ShiShang import upload_file
from datetime import datetime


class GraspChinassppSpider(scrapy.Spider):
    name = 'grasp_chinasspp'
    allowed_domains = ['www.chinasspp.com']
    start_urls = ['http://www.chinasspp.com/']
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    def start_requests(self):
        for i in range(1, 51):
            url = f'http://www.chinasspp.com/news/ss-15-{i}.html'
            req = scrapy.Request(url, callback=self.parse, dont_filter=True)
            yield req

    def parse(self, response):
        url_list = response.xpath("//div/a[@class='name']/@href").extract()
        titles = response.xpath(
            "//div/a[@class='name']/text()").extract()
        # pub_time_list = response.xpath("//ul[@class='list2']/li/i/text()").extract()
        for i in range(len(url_list)):
            url = 'http://www.chinasspp.com' + url_list[i]
            req = scrapy.Request(
                url, callback=self.parse_detail, dont_filter=True)
            news_id = request.request_fingerprint(req)
            title = titles[i]
            # pub_time = pub_time_list[i]
            req.meta.update({"news_id": news_id})
            req.meta.update({"title": title})
            # req.meta.update({"pub_time": pub_time})
            yield req

    def parse_detail(self, response):
        news_id = response.meta['news_id']
        title = response.meta['title']
        # pub_time = response.xpath("")
        # source = response.xpath(
        #     "//p[@class='inftop']/span/i/a/text()").extract_first()
        content = ''.join(response.xpath("//div[@class='n_text']").extract())
        content_img = response.xpath("//div[@class='n_text']/p/img/@src").extract()
        if content_img:
            content_img_list = list()
            for index, value in enumerate(content_img):
                img_name = title + str(index)
                res = upload_file.send_file(value, img_name, self.headers)
                if res['msg'] == 'success':
                    content = content.replace(value, res['url'][0])
                    content_img_list.append(res['url'][0])
                else:
                    self.logger.info(f'内容图片 {value} 上传失败，返回数据：{res}')

            imgs = ','.join(content_img_list)
        else:
            imgs = None
        item = ScrapyShishangItem()
        item['news_id'] = news_id
        item['category'] = '时尚'
        item['content_url'] = response.url
        item['title'] = title
        item['issue_time'] = '2022-3-20'
        item['title_image'] = None
        item['information_source'] = '时尚品牌'
        item['content'] = content
        item['source'] = '时尚品牌'
        item['author'] = None
        item['images'] = imgs
        item['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['cleaning_status'] = 0
        self.logger.info(item)
        yield item


if __name__ == '__main__':
    import scrapy.cmdline as cmd
    cmd.execute(['scrapy', 'crawl', 'grasp_chinasspp'])