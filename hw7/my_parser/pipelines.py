# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import hashlib
from pymongo.errors import DuplicateKeyError as dke


class MyParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['DB_hw7']

    def process_item(self, item, spider):
        item['_id'] = hashlib.sha256(bytes(item['url'], encoding='utf8')).hexdigest()
        col = self.mongobase[spider.name]
        item['price_sale'], item['price_true'], item['currency'] = self.process_salary(item['price'])
        try:
            col.insert_one(item)
        except dke:
            print(f'Такой контент уже есть! _id = {item["_id"]}')

        return item

    def process_salary(self, price):
        if len(price) <= 4:
            s_min = price[1]
            s_max = price[1]
            cur = price[2]
        else:
            s_min = price[1]
            s_max = price[5]
            cur = price[2]

        return s_min, s_max, cur


class MyPhotopipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [i[1] for i in results if i[0]]

        return item
