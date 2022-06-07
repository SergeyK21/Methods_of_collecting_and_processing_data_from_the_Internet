from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider
from jobparser.spiders.labirintru import LabirintruSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(
        HhruSpider,
        start_urls=[
            'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post',
            'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post'
        ],
        allowed_domains=['hh.ru']
    )
    runner.crawl(
        SuperjobruSpider,
        start_urls=[
            'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
            'https://spb.superjob.ru/vacancy/search/?keywords=python'
        ],
        allowed_domains=['superjob.ru']
    )
    runner.crawl(
        LabirintruSpider,
        start_urls=[
            'https://www.labirint.ru/books/',
            'https://www.labirint.ru/genres/1852/'
        ],
        allowed_domains=['labirint.ru']
    )

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
