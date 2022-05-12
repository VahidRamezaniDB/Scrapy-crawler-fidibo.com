from unicodedata import category
from urllib.parse import urljoin
import scrapy


class FidiboScraperSpider(scrapy.Spider):
    name = 'fidibo_scraper'
    allowed_domains = ['fidibo.com']
    start_urls = ['http://fidibo.com/']

    def start_requests(self):
        urls = [
            'http://fidibo.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categories_urls = response.xpath(
            '//*[@id="line-navbar-collapse-2"]/ul[1]/li[2]/ul/div/li/a/@href').getall()
        for url in categories_urls:
            url = urljoin(response.url, url)
            yield scrapy.Request(url, callback=self.parse_pages)
            break

    def parse_pages(self, response):

        items_urls = response.xpath(
            '/html/body/main/div/article/div/div[2]/div[2]/section[2]/div[1]/div/div/span/a/@href').getall()

        for item_url in items_urls:
            url = urljoin(self.start_urls[0], item_url)
            yield scrapy.Request(url, callback=self.parse_book)

        next_page = response.xpath(
            '//*[@id="result"]/div[2]/ul/li/a/@href').extract()

        next_page = urljoin(self.start_urls[0], next_page[-2])

        # If next_page have value
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_pages)

    def parse_book(self, response):
        title = response.xpath(
            '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/h1/a/text()').extract_first()
        if title is None:
            title = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/h1/text()').extract_first()
        book_type = response.xpath(
            '/html/body/main/div[2]/article/div[1]/div/div[3]/div/div/div[1]/a/text()'
        ).extract_first()
        if book_type == "مطالعه نسخه نمونه":
            pass
        else:
            pass
        yield {
            "title": title,
        }
