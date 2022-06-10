import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['']
    start_urls = ['']

    def __init__(self, **kwargs):
        if kwargs and isinstance(kwargs['allowed_domains'], list) and isinstance(kwargs['start_urls'], list):
            self.allowed_domains = [el for el in kwargs['allowed_domains'] if
                                    isinstance(el, str)]
            self.start_urls = [el for el in kwargs['start_urls'] if
                               isinstance(el, str)]

    def parse(self, response: HtmlResponse):
        url_str: str
        for el in self.start_urls:
            if el in response.url:
                url_str = el
                break
        next_page = url_str + response.xpath('//div[@class="pagination-next"]//a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[contains(@class, "cover")]/@href').getall()

        for link in links:
            yield response.follow('https://www.labirint.ru' + link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        print()
        name = response.xpath('//div[@id="product-title"]/h1/text()').get()
        author = response.xpath('//div[@class="authors"]/a/text()').getall()

        salary = response.xpath('//div[contains(@class,"buying-price")]//text()').getall()
        rating = response.xpath('//div[@id="rate"]/text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url, author=author, rating=rating)
