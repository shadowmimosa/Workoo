import asyncio
import logging
import random
import aiohttp

from configs import HEADERS, USER_AGENT, PARAMS
from models.db_schema import Company
from utils.split_headers import convert_headers_to_dict

logger = logging.getLogger('PROFF')


class PROFFSpider:
    headers = convert_headers_to_dict(HEADERS)

    def __init__(self, start_url):
        self.start_url = start_url
        self.domain = 'https://www.proff.no'
        self.timeout = aiohttp.ClientTimeout(total=60, connect=5)

    async def run(self):
        json_result = await self.fetch(self.start_url, params=PARAMS)
        if not json_result:
            logger.error('爬虫失败，请检查网络是否能够访问该网页')
        else:
            await self.parse(json_result)

    async def parse(self, json_result):
        search_result = json_result['createListSearchResult']
        for result in search_result['resultList']:
            name = result['displayName']
            phone_number = result['organisationNumber']

            category = ''
            for proff_industry in result['proffIndustries']:
                category += proff_industry['name'] + ','

            uri = self.domain + result['uri']
            city = result['postalAddress']['postPlace']

            try:
                Company.get(uri=uri)
            except Company.DoesNotExist:
                Company.new(uri=uri,
                            name=name,
                            phone_number=phone_number,
                            category=category,
                            city=city)

                print({'uri': uri,
                       'name': name,
                       'phone_number': phone_number,
                       'category': category.strip(','),
                       'city': city})

        next_href = search_result['pagination'].get('next')
        if not next_href:
            return

        href = next_href.get('href')
        full_url = self.domain + f'/laglister/{href}/'
        new_json_result = await self.fetch(full_url, params={'view': 'json'})
        await self.parse(new_json_result)

    async def fetch(self, url, params):
        self.headers['user-agent'] = random.choice(USER_AGENT)
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            try:
                response = await session.get(url,
                                             params=params,
                                             headers=self.headers)
            except aiohttp.ServerTimeoutError:
                logger.error('连接超时')
                return await self.fetch(url, params)

            if response.status != 200:
                logger.error('request error!!')
                return await self.fetch(url, params)

            result = await response.json()
            response.close()

        await asyncio.sleep(random.randint(2, 4))
        return result


if __name__ == '__main__':
    urls = 'https://www.proff.no/laglister'
    spider = PROFFSpider(start_url=urls)

    asyncio.run(spider.run())
