from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from my_parser.spiders.my_spider import MySpiderSpider
from my_parser.spiders.castoramaru import CastoramaruSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(
        CastoramaruSpider,
        allowed_domains=['castorama.ru'],
        start_urls=[
            'https://www.castorama.ru/catalogsearch/result/?q=%D0%BF%D0%B8%D0%BB%D0%B0&sc=nails'
        ]
    )
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


