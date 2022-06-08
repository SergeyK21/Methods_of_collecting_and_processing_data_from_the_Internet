import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from my_parser.items import MyParserItem


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
        links = response.xpath('some_xpath')
        for link in links:
            yield response.follow(link, collback=self.parse_abs)
        pass

    def parse_abs(self, response: HtmlResponse):
        loader = ItemLoader(item=MyParserItem(), response=response)
        loader.add_xpath('_id', 'some_id')
        loader.add_xpath('name', 'some_xpath')
        loader.add_xpath('name', 'some_xpath')
        yield loader.load_item()