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

        # next_page = response.xpath(
        #     '//*[@id="result"]/div[2]/ul/li/a/@href').extract()

        # next_page = urljoin(self.start_urls[0], next_page[-2])

        # # If next_page have value
        # if next_page:
        #     yield scrapy.Request(next_page, callback=self.parse_pages)

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

        if book_type is not None and "مطالعه" in book_type:

            output_dict["type"] = "کتاب الکترونیکی"

            #Author Extraction Section Begin
            author = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul/li[1]/a/span/text()').getall()
            if(len(author)==0 or author is None):
                author = "--"
            else:
                author = ', '.join(author)
            
            output_dict["author"] = author
            #Author Extraction Section End
            #Translator Extraction Section Begin
            translator = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul/li[2]/a/span/text()').getall()
            if(len(translator)==0 or translator is None):
                translator = "--"
            else:
                translator = ', '.join(translator)
            
            output_dict["translator"] = translator
            #Translator Extraction Section End
            #Narrator Extraction Section Begin

            output_dict["narrator"] = "--"

            #Narrator Extraction Section End
            #Price Extraction Section Begin
            price = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[3]/div/div/span/text()').get()
            if(price is None):
                price = "--"
            else:
                price = price.replace("تومان","",1)
            
            output_dict["price"] = price
            #Price Extraction Section End

            publisher = "--"
            pvp = "--"
            publish_date = "--"
            language = "--"
            size = "--"
            page_count = "--"
            isbn = "--"

            book_info = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li/img/@alt"
            ).getall()
            for info in book_info:
                if info == "ناشر":
                    publisher = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/a/text()", val=book_info.index(info)+1
                    ).get()
                    if publisher is None:    
                        publisher = "--"
                elif info == "تاریخ نشر":
                    publish_date = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/span/text()", val=book_info.index(info)+1
                    ).get()
                    if publish_date is None:    
                        publish_date = "--"
                elif info == "زبان":
                    language = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if language is None:    
                        language = "--"
                elif info == "حجم فایل":
                    size = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if size is None:    
                        size = "--"
                elif info == "تعداد صفحات":
                    page_count = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if page_count is None:    
                        page_count = "--"
                elif info == "شابک":
                    isbn = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/label/text()", val=book_info.index(info)+1
                    ).get()
                    if isbn is None:    
                        isbn = "--"
                elif info == "قیمت نسخه چاپی":
                    pvp = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/span/text()", val=book_info.index(info)+1
                    ).get()
                    if pvp is None:    
                        pvp = "--"
            output_dict["publisher"] = publisher
            output_dict["pvp"] = pvp
            output_dict["publish date"] = publish_date
            output_dict["language"] = language
            output_dict["size"] = size
            output_dict["page count"] = page_count
            output_dict["ISBN"] = isbn




            #Publisher Exctraction Section Begin

            # publisherIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[1]/img/@alt').get()
            
            # if(publisherIndicator == "ناشر"):
            #     publisher = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[1]/a/text()').extract_first()
            # else:
            #     publisher = "--"
            
            # if(publisher is None):
            #     publisher = "--"
            # else:
            #     #Publisher Normalization code goes here
            #     pass

            # output_dict["publisher"] = publisher
            # #Publisher Extraction Section End
            # #Pvp Extraction Section Begin
            # pvpIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[2]/img/@alt').get()

            # if(pvpIndicator == "قیمت نسخه چاپی"):
            #     pvp = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[2]/span/text()').extract_first()
            # else:
            #     pvp = "--"
            
            # if(pvp is None):
            #     pvp = "--"
            # else:
            #     #Pvp Normalization code goes here
            #     pass

            # output_dict["pvp"] = pvp
            # #Pvp Extraction Section End
            # #Publish Date Extraction Section Begin
            # pdIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[3]/img/@alt').get()

            # if(pdIndicator == "تاریخ نشر"):
            #     pdate = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[3]/span/text()').extract_first()
            # else:
            #     pdate = "--"
            
            # if(pdate is None):
            #     pdate = "--"
            
            # output_dict["publish date"] = pdate
            # #Publish Date Extraction Section End
            # #Language Extraction Section Begin

            # langIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[4]/img/@alt').get()

            # if(langIndicator == "زبان"):
            #     language = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[4]/text()').extract_first()
            # else:
            #     language = "--"
            
            # if(language is None):
            #     language = "--"

            # output_dict["language"] = language

            # #Language Extraction Section End
            # #size Extraction Section Begin

            # sizeIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[5]/img/@alt').get()

            # if(sizeIndicator == "حجم فایل"):
            #     size = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[5]/text()').extract_first()
            # else:
            #     size = "--"
            
            # if(size is None):
            #     size = "--"
            # else:
            #     #size Normalization code goes here
            #     pass

            # output_dict["size"] = size
            # #size Extraction Section End
            # #Pages Extraction Section Begin

            # pagesIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[6]/img/@alt').get()

            # if(pagesIndicator == "تعداد صفحات"):
            #     pages = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[6]/text()').extract_first()
            # else:
            #     pages = "--"
            
            # if(pages is None):
            #     pages = "--"
            # else:
            #     #pages Normalization code goes here
            #     pass

            # output_dict["page count"] = pages
            # #Pages Extraction Section End
            # #ISBN Extraction Section Begin

            # isbnIndicator = response.xpath(
            #     '/html/body/main/div[2]/section/div/div/ul/li[7]/img/@alt').get()

            # if(isbnIndicator == "شابک"):
            #     ISBN = response.xpath(
            #         '/html/body/main/div[2]/section/div/div/ul/li[7]/label/text()').extract_first()
            # else:
            #     ISBN = "--"
            
            # if(ISBN is None):
            #     ISBN = "--"

            # output_dict["ISBN"] = ISBN
            #ISBN Extraction Section End
            #Description Extraction Section Begin

            # description = response.xpath(
            #     '/html/body/main/div[2]/article/section/div/section/div/p[1]/text()').get()
            # if(description is None):
            #     description = response.xpath(
            #         '/html/body/main/div[2]/article/section/div/div/div[1]/p/text()').get()
            # if(description is None):
            #     description = "--"
            # output_dict["description"] = description

            description = response.xpath(
                "/html/body/main/div[2]/article/section/div/div/div[1]/p/text()"
            ).get()
            if description is None:
                description = response.xpath(
                    "/html/body/main/div[2]/article/section/div/section/div/p[1]/text()"
                ).get()
            if description is None:
                description = "--"
            output_dict["description"] = description

            #Description Extraction Section End
            #Category Extraction Section Begin

            bookCategories = response.xpath(
                '/html/body/div[1]/nav/ul/li/a/span/text()').getall()
            if (bookCategories is None):
                bookCategories = "--"
            else:
                bookCategories.pop(0)
                bookCategories = ", ".join(bookCategories)

            output_dict["category"] = bookCategories

            #Category Extraction Section End
            #Cover Extraction Section Begin

            cover = response.xpath(
                '/html/body/main/div[2]/article/div[1]/div/div[1]/div/img/@src').get()
            if (cover is None):
                cover = "--"

            output_dict["cover"] = cover

            #Cover Extraction Section End
            pass
        elif book_type is not None:
            output_dict['type'] = "کتاب صوتی"


            author = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul/li[1]/a/span/text()"
            ).getall()
            if author is None or len(author)==0:
                author = "--"
            else:
                author = ','.join(author)            
            output_dict["author"] = author


            translator = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul[1]/li[2]/a/span/text()"
            ).getall()
            if translator is None or len(translator)==0:
                translator = "--"
            else:
                translator = ','.join(translator)            
            output_dict["translator"] = translator


            narrator = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[2]/div/div/div[1]/ul[1]/li[3]/a/span/text()"
            ).getall()
            if narrator is None or len(narrator)==0:
                narrator = "--"
            else:
                narrator = ','.join(narrator)            
            output_dict["narrator"] = narrator


            price = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[3]/div/div/span/text()"
            ).get()
            if price is None:
                price = "--"
            else:
                price = price.replace("تومان","",1)
            output_dict["price"] = price


            publisher = "--"
            pvp = "--"
            publish_date = "--"
            language = "--"
            size = "--"
            page_count = "--"
            isbn = "--"

            book_info = response.xpath(
                "/html/body/main/div[2]/section/div/div/ul/li/img/@alt"
            ).getall()
            for info in book_info:
                if info == "ناشر":
                    publisher = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/a/text()", val=book_info.index(info)+1
                    ).get()
                    if publisher is None:    
                        publisher = "--"
                elif info == "تاریخ نشر":
                    publish_date = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/span/text()", val=book_info.index(info)+1
                    ).get()
                    if publish_date is None:    
                        publish_date = "--"
                elif info == "زبان":
                    language = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if language is None:    
                        language = "--"
                elif info == "حجم فایل":
                    size = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if size is None:    
                        size = "--"
                elif info == "تعداد صفحات":
                    page_count = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/text()", val=book_info.index(info)+1
                    ).get()
                    if page_count is None:    
                        page_count = "--"
                elif info == "شابک":
                    isbn = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/label/text()", val=book_info.index(info)+1
                    ).get()
                    if isbn is None:    
                        isbn = "--"
                elif info == "قیمت نسخه چاپی":
                    pvp = response.xpath(
                        "/html/body/main/div[2]/section/div/div/ul/li[$val]/span/text()", val=book_info.index(info)+1
                    ).get()
                    if pvp is None:    
                        pvp = "--"
            output_dict["publisher"] = publisher
            output_dict["pvp"] = pvp
            output_dict["publish date"] = publish_date
            output_dict["language"] = language
            output_dict["size"] = size
            output_dict["page count"] = page_count
            output_dict["ISBN"] = isbn

            # publisher_img = response.xpath(
            #     "/html/body/main/div[2]/section/div/div/ul/li[1]/img/@alt"
            # ).get()
            # if publisher_img == "ناشر":
            #     publisher = response.xpath(
            #         "/html/body/main/div[2]/section/div/div/ul/li[1]/a/text()"
            #     ).get()
            #     if publisher is None:
            #         publisher = "--"    
            #     output_dict["publisher"] = publisher
            # else:
            #     output_dict["publisher"] = "--"

            
            # output_dict["pvp"] = "--"


            # publish_date_img = response.xpath(
            #     "/html/body/main/div[2]/section/div/div/ul/li[2]/img/@alt"
            # ).get()
            # if publish_date_img == 'تاریخ نشر':
            #     publish_date = response.xpath(
            #         "/html/body/main/div[2]/section/div/div/ul/li[2]/span/text()"
            #     ).get()
            #     if publish_date is None:
            #         publish_date = "--"
            #     output_dict["publish date"] = publish_date
            # else:
            #     output_dict["publish date"] = "--"

            
            # language_img = response.xpath(
            #     "/html/body/main/div[2]/section/div/div/ul/li[3]/img/@alt"
            # ).get()
            # if language_img == 'زبان':
            #     language = response.xpath(
            #         "/html/body/main/div[2]/section/div/div/ul/li[3]/text()"
            #     ).get()
            #     if language is None:
            #         language = "--"
            #     output_dict["language"] = language
            # else:
            #     output_dict["language"] = "--"
            

            # size_img = response.xpath(
            #     "/html/body/main/div[2]/section/div/div/ul/li[4]/img/@alt"
            # ).get()
            # if size_img == "حجم فایل":
            #     size = response.xpath(
            #         "/html/body/main/div[2]/section/div/div/ul/li[4]/text()"
            #     ).get()
            #     if size is None:
            #         size = "--"
            #     output_dict["size"] = size
            # else:
            #     output_dict["size"] = "--"

            
            # output_dict["page count"] = "--"
            # output_dict["ISBN"] = "--"


            description = response.xpath(
                "/html/body/main/div[2]/article/section/div/div/div[1]/p/text()"
            ).get()
            if description is None:
                description = response.xpath(
                    "/html/body/main/div[2]/article/section/div/section/div/p[1]/text()"
                ).get()
            if description is None:
                description = "--"
            output_dict["description"] = description


            book_cat = response.xpath(
                "/html/body/div[1]/nav/ul/li/a/span/text()"
            ).getall()
            if book_cat is None or len(book_cat) == 0:
                book_cat = "--"
            else:
                book_cat.pop(0)
                book_cat = ','.join(book_cat)
            output_dict["category"] = book_cat


            cover = response.xpath(
                "/html/body/main/div[2]/article/div[1]/div/div[1]/div/img[1]/@src"
            ).get()
            if cover is None:
                cover = "--"
            output_dict["cover"] = cover

        yield output_dict
