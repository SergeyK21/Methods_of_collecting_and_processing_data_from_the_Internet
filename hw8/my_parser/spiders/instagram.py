import scrapy
from scrapy.http import HtmlResponse
import re


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_name = 'study.ai_172'
    insta_pwd = ''
    inst_login_link = ''
    user_for_parse = ''

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={
                'enc_password': self.insta_pwd,
                'username': self.insta_name
            },
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.user_for_parse}',
                callback=self.user_data,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_data(self, response: HtmlResponse, **kwargs):
        pass

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
