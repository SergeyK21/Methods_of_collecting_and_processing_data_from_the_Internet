import scrapy
from scrapy.http import HtmlResponse


class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['']
    start_urls = ['']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs and isinstance(kwargs['allowed_domains'], list) and isinstance(kwargs['start_urls'], list):
            self.allowed_domains = [el for el in kwargs['allowed_domains'] if
                                    isinstance(el, str)]
            self.start_urls = [el for el in kwargs['start_urls'] if
                               isinstance(el, str)]

    def parse(self, response: HtmlResponse):
        print()
        pass

