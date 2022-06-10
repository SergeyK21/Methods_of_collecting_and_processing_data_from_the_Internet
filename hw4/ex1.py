"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
2. Сложить собранные новости в БД
Минимум один сайт, максимум - все три
"""

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import requests
import time
from pprint import pprint
import hashlib
from lxml import html


def get_news_mail() -> list:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    response = requests.get('https://news.mail.ru/', headers=headers)

    result = []

    dom = html.fromstring(response.text)
    links_news = dom.xpath("//a[@class='list__text']/@href")
    news_name = dom.xpath("//a[@class='list__text']/text()")
    for i, link_news in enumerate(links_news):
        time.sleep(1)
        temp = {}
        temp['_id'] = hashlib.sha256(bytes(link_news, encoding='utf8')).hexdigest()
        temp['news_link'] = link_news
        temp['news_name'] = news_name[i]
        response = requests.get(link_news, headers=headers)
        dom = html.fromstring(response.text)
        date = dom.xpath(
            ".//div[contains(@class,'article js-article')]/div[contains(@class,'breadcrumbs breadcrumbs_article')]//span[contains(@class,'note__text breadcrumbs__text js-ago')]/@datetime")
        temp['news_date'] = date
        source_name = dom.xpath(
            ".//div[contains(@class,'article js-article')]/div[contains(@class,'breadcrumbs breadcrumbs_article')]//span[contains(@class,'link__text')]/text()")
        temp['news_source'] = source_name
        result.append(temp)
    return result





def create_collection_in_databese_mogo(collection_name:str, news_list: list, database_name: str = 'my_mongoDB'):
    '''
    collection_name: Наименование коллекции;
    news_list: контент;
    database_name: Наименование базы данных (по умолчанию "my_mongoDB").
    '''

    client = MongoClient('127.0.0.1', 27017)
    db = client[database_name]

    col = db[collection_name]

    for i, el in enumerate(news_list):
        try:
            col.insert_one(el)
        except dke:
            print('Есть такой контент!')

    client.close()


if __name__ == '__main__':

    collection_name='news_mail'

    create_collection_in_databese_mogo(collection_name,get_news_mail())

    client = MongoClient('127.0.0.1', 27017)
    db = client['my_mongoDB']

    col = db[collection_name]
    for doc in col.find({}):
        pprint(doc)

