# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from douban.settings import mongo_db_collection,mongo_db_name,mongo_host,mongo_port

class DoubanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        db_name = mongo_db_name
        db_collection = mongo_db_collection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[db_name]
        self.post = mydb[db_collection]

    def process_item(self, item, spider):
        # 需要先把item的数据转化为字典的形式
        data = dict(item)
        # 将拿到的数据插入到数据库
        self.post.insert(data)
        return item
