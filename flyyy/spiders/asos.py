from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import random
import time

class Asos(scrapy.Spider):
    name = "asos"
    allowed_domains = ["asos.com"]
    start_urls = []
    sitemaps = []

    sitemap_main = ["http://www.asos.com/au/sitemap.ashx"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
      sitemaps.append(main_tag.findNext("loc").text)

    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            prod_link = tag.findNext("loc").text
            if '?iid=' in prod_link:
                start_urls.append(prod_link)
    start_urls = start_urls[0:25]
    au = 0
    for url in start_urls:
      if 'au.asos' in url:
        au +=1

    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['brand'] = "" #Needs post-processing!

        item['cat_code'] = ""
        item['cat_1'] = "" #deprecate
        item['cat_2'] = "" #deprecate
        item['cat_3'] = "" #deprecate

        item['currency'] = response.selector.xpath('//div[@class="currency"]/span[@class="code"]/text()').extract()[0]
        item['currency_code'] = response.selector.xpath('//*[@class="currency_list"]//*[@selected="selected"]/text()').extract()
        item['merchant_country']
        item['language']

        item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

        item['is_available'] = True #Don't change! #Fix later!
        item['affiliate_partner'] = "viglink"

        item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999)))) #Don't change!
        item['product_link'] = response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]

        item['merchant_prod_id'] = response.selector.xpath('//div[@id="product-detail"]/div[@class="product-name"]/@id').extract()[0][2:]
        item['merchant_id'] = "3O056R"


        item['short_desc'] = response.selector.xpath('//div[@id="product-detail"]/div[@class="product-name"]/h1/text()').extract()[0]
        item['long_desc'] = response.selector.xpath('//div[@itemprop="description"]/p/text()').extract()[0].strip()
        item['primary_color'] = "" #later


        #If item is on sale,

        try:
            if (int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[@class="sale"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[@class="retail"]/text()').extract()[0][1:]))):
                orig = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[@class="retail"]/text()').extract()[0][1:]))
                sale = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[@class="sale"]/text()').extract()[0][1:]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
            else:
                item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[@class="retail"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/text()').extract()[0][1:]))
            item['price'] = item['price_orig']

        item['image_urls'] = response.selector.xpath('//ul[@id="image-carousel"]/li/a/@href').extract()
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        item['mcats'] = "" #later #Do NLP predictions



        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)



        yield item