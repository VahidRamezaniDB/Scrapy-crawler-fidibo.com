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
        output_dict = {}

        title = response.xpath(
            '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/h1/a/text()').extract_first()
        if title is None:
            title = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/h1/text()').extract_first()
        
        output_dict["title"] = title

        book_type = response.xpath(
            '/html/body/main/div[2]/article/div[1]/div/div[3]/div/div/div[1]/a/text()'
        ).extract_first()

        if book_type == "مطالعه نسخه نمونه":
            pass
        else:
            output_dict['type'] = "کتاب صوتی"


            author = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul/li[1]/a/span/text()"
            ).getall()
            if author is None or len(author)==0:
                author = "اطلاعات موجود نیست."
            else:
                author = ','.join(author)            
            output_dict["author"] = author


            translator = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul[1]/li[2]/a/span/text()"
            ).getall()
            if translator is None or len(translator)==0:
                translator = "اطلاعات موجود نیست."
            else:
                translator = ','.join(translator)            
            output_dict["translator"] = translator


            narrator = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul[1]/li[3]/a/span/text()"
            ).getall()
            if narrator is None or len(narrator)==0:
                narrator = "اطلاعات موجود نیست."
            else:
                narrator = ','.join(narrator)            
            output_dict["narrator"] = narrator


            price = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[3]/div/div/span/text()"
            ).get()
            if price is None:
                price = "اطلاعات موجود نیست."
            output_dict["price"] = price


            publisher_img = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li[1]/img/@alt"
            ).get()
            if publisher_img == "ناشر":
                publisher = response.xpath(
                    "/html/body/main/div[2]/section/div/div/ul/li[1]/a/text()"
                ).get()
                if publisher is None:
                    publisher = "اطلاعات موجود نیست."    
                output_dict["publisher"] = publisher
            else:
                output_dict["publisher"] = "اطلاعات موجود نیست."

            
            output_dict["pvp"] = "اطلاعات موجود نیست."


            publish_date_img = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li[2]/img/@alt"
            ).get()
            if publish_date_img == 'تاریخ نشر':
                publish_date = response.xpath(
                    "/html/body/main/div[2]/section/div/div/ul/li[2]/span/text()"
                ).get()
                if publish_date is None:
                    publish_date = "اطلاعات موجود نیست."
                output_dict["publish date"] = publish_date
            else:
                output_dict["publish date"] = "اطلاعات موجود نیست."

            
            language_img = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li[3]/img/@alt"
            ).get()
            if language_img == 'زبان':
                language = response.xpath(
                    "/html/body/main/div[2]/section/div/div/ul/li[3]/text()"
                ).get()
                if language is None:
                    language = "اطلاعات موجود نیست."
                output_dict["language"] = language
            else:
                output_dict["language"] = "اطلاعات موجود نیست."
            

            size_img = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li[4]/img/@alt"
            ).get()
            if size_img == "حجم فایل":
                size = response.xpath(
                    "/html/body/main/div[2]/section/div/div/ul/li[4]/text()"
                ).get()
                if size is None:
                    size = "اطلاعات موجود نیست."
                output_dict["size"] = size
            else:
                output_dict["size"] = "اطلاعات موجود نیست."

            
            output_dict["page count"] = "اطلاعات موجود نیست."
            output_dict["ISBN"] = "اطلاعات موجود نیست."


            description = response.xpath(
                "/html/body/main/div[2]/article/section/div/div/div[1]/p/text()"
            ).get()
            if description is None:
                description = response.xpath(
                    "/html/body/main/div[2]/article/section/div/section/div/p[1]/text()"
                ).get()
            if description is None:
                description = "اطلاعات موجود نیست."
            output_dict["description"] = description


            book_cat = response.xpath(
                "/html/body/div[1]/nav/ul/li/a/span/text()"
            ).getall()
            if book_cat is None or len(book_cat) == 0:
                book_cat = "اطلاعات موجود نیست."
            else:
                book_cat.pop(0)
                book_cat.pop(len(book_cat)-1)
                book_cat = ','.join(book_cat)
            output_dict["category"] = book_cat


            cover = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[1]/div/img[1]/@src"
            ).get()
            if cover is None:
                cover = "اطلاعات موجود نیست."
            output_dict["cover"] = cover

        yield output_dict
