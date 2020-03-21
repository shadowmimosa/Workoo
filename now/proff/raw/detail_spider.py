from spider.domain_spider import DomainSpider
from models.db_schema import Company


class Crawl:
    def run_spiders(self):
        start_urls = self.fetch_urls()
        if not start_urls:
            return

        spider = DomainSpider(start_urls=start_urls)
        spider.run()

    def fetch_urls(self):
        company = Company.select()

        start_urls = [
            _company.uri for _company in company
        ]
        return start_urls


def main():
    crawl = Crawl()
    crawl.run_spiders()


if __name__ == '__main__':
    main()
