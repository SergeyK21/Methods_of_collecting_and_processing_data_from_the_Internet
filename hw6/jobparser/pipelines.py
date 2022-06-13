# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import hashlib

from pymongo.errors import DuplicateKeyError as dke


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase_vacancy = client['vacancyDB']
        self.mongobase_books = client['booksDB']

    def process_item(self, item, spider):
        print()
        item['_id'] = hashlib.sha256(bytes(item['url'], encoding='utf8')).hexdigest()
        if spider.name == 'hhru' or spider.name == 'superjobru':
            if spider.name == 'hhru':
                item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_hh(item['salary'])
            else:
                item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sj(item['salary'])
            col = self.mongobase_vacancy[spider.name]
            try:
                col.insert_one(item)
            except dke:
                print(f'Такой контент уже есть! _id = {item["_id"]}')
        else:
            if spider.name == 'labirintru':
                item['price_real'], item['price_sale'], item['currency'] = self.process_price_lab(item['price'])
            else:
                pass
            col = self.mongobase_books[spider.name]
            try:
                col.insert_one(item)
            except dke:
                print(f'Такой контент уже есть! _id = {item["_id"]}')

        return item

    def process_salary_hh(self, salary):
        s_min = None
        s_max = None
        cur = None
        if len(salary) == 8:
            s_min = int("".join([i for i in salary[1].split() if i.isdigit()]))
            s_max = int("".join([i for i in salary[3].split() if i.isdigit()]))
            cur = salary[5]
        elif len(salary) == 6:
            if 'от' in salary[0]:
                s_min = int("".join([i for i in salary[1].split() if i.isdigit()]))
                cur = salary[3]
            else:
                s_max = int("".join([i for i in salary[1].split() if i.isdigit()]))
                cur = salary[3]

        return s_min, s_max, cur

    def process_salary_sj(self, salary):
        s_min = None
        s_max = None
        cur = None
        if len(salary) == 9:
            s_min = int("".join([i for i in salary[0].split() if i.isdigit()]))
            s_max = int("".join([i for i in salary[4].split() if i.isdigit()]))
            cur = salary[6]
        elif len(salary) == 5:
            if 'от' in salary[0]:
                temp = salary[2].split('\xa0')
                temp_str = ''.join(temp)
                s_min = int("".join([i for i in temp_str if i.isdigit()]))
                cur = temp[-1]
            elif 'до' in salary[0]:
                temp = salary[2].split('\xa0')
                temp_str = ''.join(temp)
                s_max = int("".join([i for i in temp_str if i.isdigit()]))
                cur = temp[-1]
            else:
                temp = salary[0].split('\xa0')
                temp_str = ''.join(temp)
                s_max = int("".join([i for i in temp_str if i.isdigit()]))
                cur = salary[2]

        return s_min, s_max, cur

    def process_price_lab(self,price):
        price_real = None
        price_sale = None
        currency = None
        if len(price) == 14:
            price_real = int("".join([i for i in price[3] if i.isdigit()]))
            price_sale = int("".join([i for i in price[9] if i.isdigit()]))
            currency = price[11]
        elif len(price) == 7:
            price_real = int("".join([i for i in price[3] if i.isdigit()]))
            currency = price[5]
        return price_real, price_sale, currency

