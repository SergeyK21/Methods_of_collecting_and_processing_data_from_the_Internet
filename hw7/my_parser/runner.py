from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from my_parser.spiders.my_spider import MySpiderSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(
        MySpiderSpider,
        start_urls=[
            'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post',
            'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post'
        ],
        allowed_domains=['hh.ru']
    )

