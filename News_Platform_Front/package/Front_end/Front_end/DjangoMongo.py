"""
@Description :
@File        : DjangoMongo
@Project     : Front_end
@Time        : 2022/4/13 11:21
@Author      : LiHouJian
@Software    : PyCharm
@issue       :
@change      :
@reason      :
"""

import pymongo
from urllib import parse


col_cate_map = {
    '财经': 'CaiJing_DB',
    '科技': 'KeJi_DB',
    '娱乐': 'YuLe_DB',
    '体育': 'TiYu_DB',
    '时尚': 'ShiShang_DB',
    '美食': 'MeiShi_DB',
    '国际': 'GuoJi_DB',
    '养生': 'YangSheng',
    '旅游': 'LvYou_DB',
}


class Get_data_from_mongo():
    def __init__(self):
        username = parse.quote_plus('storm')  # 对用户名进行编码
        password = parse.quote_plus('98765432.zx')  # 对密码进行编码
        database = "News_Dbs"  # 数据库名称
        host = "175.24.172.64"
        port = "27017"

        client = pymongo.MongoClient(
            'mongodb://%s:%s@%s:%s/' %
            (username, password, host, port))
        self.mydb = client[database]

    def get_info(self, cate):
        """
        :param cate:
        :return: info_list
        """
        col = col_cate_map.get(cate)
        my_collection = self.mydb[col]
        news_interval = my_collection.find().limit(60)
        news_interval_list = list()
        for item in news_interval:
            news_interval_list.append(item)
        return news_interval_list

    def get_single_info_by_news_id(self, news_id, cate):
        """
        :param news_id: 集合字段news_id
        :param cate: 集合字段category
        :return: a single doc
        """
        col = col_cate_map.get(cate)
        my_collection = self.mydb[col]
        single_info = my_collection.find_one({'news_id': news_id})
        return single_info

    def get_newest_info_from_all_col(self):
        """
        :return: newest info from each collection
        """
        info_list = list()
        # col = 'KeJi_DB'
        for col in col_cate_map.values():
            my_collection = self.mydb[col]
            newest_info = my_collection.find().sort('issue_time', -1).limit(1)
            for info in newest_info:
                info_list.append(info)
        return info_list

    def get_the_fuzzy_data(self, key_words):
        """
        :param key_words:
        :return: the_fuzzy_data
        """
        the_fuzzy_data = list()
        for col in col_cate_map.values():
            the_fuzzy_data_temp = self.mydb[col].find({"title": {'$regex': key_words}})
            for info in the_fuzzy_data_temp:
                the_fuzzy_data.append(info)
        return the_fuzzy_data


