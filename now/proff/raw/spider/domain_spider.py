import logging
import random

import requests

from lxml import etree
from configs import HEADERS, USER_AGENT
from models.db_schema import Company
from utils.split_headers import convert_headers_to_dict

logger = logging.getLogger('proff.no')


class DomainSpider:
    headers = convert_headers_to_dict(HEADERS)

    def __init__(self, start_urls: list):
        self.start_urls = start_urls

        self.retry_times = 5

    def run(self):
        for url in self.start_urls:
            html = self.fetch(url)
            if html:
                self.retry_times = 5
                self.parse(html, url)

    def parse(self, html, url):
        try:
            company = Company.get(uri=url)
        except Company.DoesNotExist:
            logger.error(f'{url} 未存在数据库中')
            return

        selector = etree.HTML(html)

        domain_result = selector.xpath('//a[contains(@class, "addax-cs_ip_homepage_url_click")]/text()')
        domain = domain_result[0] if domain_result else ''

        email_result = selector.xpath('string(//a[contains(@class, "addax-cs_ip_email_click")]/span)')
        email = email_result if email_result else ''

        company.update_detail(domain=domain, email_address=email)

    def fetch(self, url):
        self.headers['user-agent'] = random.choice(USER_AGENT)
        try:
            response = requests.get(url,
                                    headers=self.headers,
                                    timeout=10)
        except requests.RequestException as error:
            logger.error(error)
            return self.retry(url)

        if response.status_code != 200:
            logger.error('request error!!')
            return self.retry(url)

        result = response.text.encode(response.encoding).decode('utf-8')
        return result

    def retry(self, url):
        if 0 < self.retry_times:
            self.retry_times -= 1
            print(f'获取失败，第{5 - self.retry_times}次重试')

            return self.fetch(url)
        else:
            self.retry_times = 5
            print(f'{url} 重试5次获取失败')
            return None
