import scrapy


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['']
    start_urls = ['']

    def parse(self, response):
        pass
