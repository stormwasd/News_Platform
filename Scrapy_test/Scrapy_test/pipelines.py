# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
# from scrapy.conf import settings
from Scrapy_test.items import ScrapyTestItem


class ScrapyTestPipeline(object):
	def __init__(self, mongourl, mongoport, mongodb, mongodocname):
		client = pymongo.MongoClient(mongourl, mongoport)
		db = client[mongodb]
		self.connection = db[mongodocname]

	@classmethod
	def from_crawler(cls, crawler):
		"""
		1、读取settings里面的mongodb数据的url、port、DB。
		:param crawler:
		:return:
		"""
		return cls(
			mongourl=crawler.settings.get("MONGO_DB_URL"),
			mongoport=crawler.settings.get("MONGO_DB_PORT"),
			mongodb=crawler.settings.get("MONGO_DB_NAME"),
			mongodocname = crawler.settings.get("MONGODB_DOCNAME")
		)

	def process_item(self, item, spider):
		""" 判断item的类型，并作相应的处理，再入数据库 """
		try:
			if isinstance(item, ScrapyTestItem):
				# ~ self.newBookDetail.insert(dict(item))
				self.connection.insert({'news_id': item['news_id'], 'category': item['category'], 'content_url': item['content_url'], 'title': item['title'], 'issue_time': item['issue_time'], 'title_image': item['title_image'], 'information_source': item['information_source'], 'source': item['source'], 'author': item['author'], 'content': item['content'], 'images': item['images'], 'update_time': item['update_time'], 'cleaning_status': item['cleaning_status']}, {'$set': dict(item)})
			else:
				# ~ self.newBookDetail.insert(item)
				self.connection.insert({'news_id': item['news_id'], 'category': item['category'], 'content_url': item['content_url'], 'title': item['title'], 'issue_time': item['issue_time'], 'title_image': item['title_image'], 'information_source': item['information_source'], 'source': item['source'], 'author': item['author'], 'content': item['content'], 'images': item['images'], 'update_time': item['update_time'], 'cleaning_status': item['cleaning_status']}, {'$set': item})
		except Exception as e:
			print(e)
		return item
