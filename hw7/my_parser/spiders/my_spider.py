import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from my_parser.items import MyParserItem

import hashlib


class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs and isinstance(kwargs['allowed_domains'], list) and isinstance(kwargs['start_urls'], list):
            self.allowed_domains = [el for el in kwargs['allowed_domains'] if
                                    isinstance(el, str)]
            self.start_urls = [el for el in kwargs['start_urls'] if
                               isinstance(el, str)]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//body/div[@id='__aer_root__']/div[1]/div[3]/div[1]/div[2]/div[1]/div[4]/button[9]").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[@class="SearchProductFeed_ProductSnippet__content__7lwrv"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_abs)


    def parse_abs(self, response: HtmlResponse):
        loader = ItemLoader(item=MyParserItem(), response=response)
        loader.add_value('_id', hashlib.sha256(bytes(response.url, encoding='utf8')).hexdigest())
        loader.add_xpath('name', "//body/div[@id='__aer_root__']/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/h1/text()")
        loader.add_xpath('price', "///body/div[@id='__aer_root__']/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]//text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//body/div[@id='__aer_root__']/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//img/@src")
        yield loader.load_item()
