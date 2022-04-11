"""
@Description : 
@File        : grasp_fashion_huanqiu
@Project     : Scrapy_ShiShang
@Time        : 2022/4/11 18:35
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
from jsonpath import jsonpath


class GraspFashionHuanqiuSpider(scrapy.Spider):
	name = 'grasp_fashion_huanqiu'
	allowed_domains = ['fashion.huanqiu.com']
	# start_urls = ['http://www.chinasspp.com/']
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
	}

	def start_requests(self):
		for i in range(0, 51):
			url = f'https://fashion.huanqiu.com/api/list2?node=/e3pn4vu2g/e3pn4vuih&offset={i * 20}&limit=20'
			headers = {
				'authority': 'fashion.huanqiu.com',
				'pragma': 'no-cache',
				'cache-control': 'no-cache',
				'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
				'accept': '*/*',
				'x-requested-with': 'XMLHttpRequest',
				'sec-ch-ua-mobile': '?0',
				'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
				'sec-ch-ua-platform': '"Windows"',
				'sec-fetch-site': 'same-origin',
				'sec-fetch-mode': 'cors',
				'sec-fetch-dest': 'empty',
				'referer': 'https://fashion.huanqiu.com/news',
				'accept-language': 'zh-CN,zh;q=0.9',
				'cookie': 'UM_distinctid=17e285262523df-08157b5f21e45f-3b39580e-384000-17e28526253830; _ga=GA1.2.1420258345.1646375558; Hm_lvt_1fc983b4c305d209e7e05d96e713939f=1649671461; REPORT_UID_=WZpnfnflfucUlObu9jrEayimzCN4rTna; CNZZDATA1000010102=315537858-1649664515-https%253A%252F%252Fwww.baidu.com%252F%7C1649669035; Hm_lpvt_1fc983b4c305d209e7e05d96e713939f=1649673207'
			}
			req = scrapy.Request(url, callback=self.parse, dont_filter=True, headers=headers)
			yield req

	def parse(self, response):
		url_list_ids = jsonpath(response, '$..aid')
		titles = jsonpath(response, '$..title')
		# ctime
		pub_time_list = jsonpath(response, '$..ctime')
		for i in range(len(url_list)):
			url = url_list[i]
			req = scrapy.Request(
				url, callback=self.parse_detail, dont_filter=True)
			news_id = request.request_fingerprint(req)
			title = titles[i]
			pub_time = pub_time_list[i]
			req.meta.update({"news_id": news_id})
			req.meta.update({"title": title})
			req.meta.update({"pub_time": pub_time})
			yield req
