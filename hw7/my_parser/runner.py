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
        allowed_domains=['avito.ru'],
        start_urls=[
            'https://www.avito.ru/moskva?localPriority=0&q=iphone'
        ]

    )
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
