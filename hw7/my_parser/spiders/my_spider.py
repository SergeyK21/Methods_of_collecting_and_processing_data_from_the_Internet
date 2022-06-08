import scrapy


class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['x']
    start_urls = ['http://x/']

    def parse(self, response):
        pass
