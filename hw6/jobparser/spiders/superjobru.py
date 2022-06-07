import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['']
    start_urls = ['']

    def __init__(self, **kwargs):
        if kwargs and isinstance(kwargs['allowed_domains'], list) and isinstance(kwargs['start_urls'], list):
            self.allowed_domains = [el for el in kwargs['allowed_domains'] if
                                    isinstance(el, str)]
            self.start_urls = [el for el in kwargs['start_urls'] if
                               isinstance(el, str)]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@class="_1IHWd _6Nb0L _37aW8 _2qMLS f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="_5isIP _1O2dw _2hWnG L6dwW"]//a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        print()
        name = response.xpath('//h1[@class="_1OayW _3SX72 _1tWy- PMNMn _1_L5R z4PWH _2Rwtu"]//text()').get()
        salary = response.xpath('//div[@class="_5isIP _23tdv _3s_fn _3fduN _1n-xi nsf4m _3sYO7 _1a_t2"]//span[@class="_4Gt5t _2nJZK"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)