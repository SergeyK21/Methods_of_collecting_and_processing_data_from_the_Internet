# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clear_price(value: str):
    if value:
        value = value.replace('\xa0', '')
        try:
            value = int("".join([i for i in value.split() if i.isdigit()]))
        except Exception as e:
            return value
        return value



class MyParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price_sale = scrapy.Field()
    price_true = scrapy.Field()
    currency = scrapy.Field()

