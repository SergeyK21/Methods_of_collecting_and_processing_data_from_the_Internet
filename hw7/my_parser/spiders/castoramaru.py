import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from my_parser.items import MyParserItem
import hashlib


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs and isinstance(kwargs['allowed_domains'], list) and isinstance(kwargs['start_urls'], list):
            self.allowed_domains = [el for el in kwargs['allowed_domains'] if
                                    isinstance(el, str)]
            self.start_urls = [el for el in kwargs['start_urls'] if
                               isinstance(el, str)]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[contains(@class, "toolbar-bottom")]//a[@class="next_jump"]').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            '//li[contains(@class, "product-card ")]/a[contains(@class,"product-card__name")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_abs)

    def parse_abs(self, response: HtmlResponse):
        loader = ItemLoader(item=MyParserItem(), response=response)
        loader.add_xpath('name',
                         "//h1[contains(@class,'product-essential__name')]/text()")
        loader.add_xpath('price',
                         '//form[@class="add-to-cart"]//div[contains(@class, "add-to-cart__price")]//span//text()')
        loader.add_value('url', response.url)
        loader.add_xpath('photos',
                         '//ul[@class="swiper-wrapper"]//div/img/@data-src')
        yield loader.load_item()
