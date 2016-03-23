from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime

class TheOutnet(scrapy.Spider):
    name = "the-outnet"
    allowed_domains = ["theoutnet.com"]
    start_urls = []
    sitemaps = []

    sitemap_main = ["https://www.theoutnet.com/sitemap.xml"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
        sitemaps.append(main_tag.findNext("loc").text)

    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            prod_link = tag.findNext("loc").text
            start_urls.append(prod_link)


    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!

        item['affiliate_partner'] = "viglink"
        item['brand'] = response.selector.xpath('//div[@id="product-heading"]/h1/a/text()').extract()[0]
        item['long_desc'] = " | ".join(response.selector.xpath('//li[@id="details-section"]/ul/li/div[@class="tab-details translateSection"]/ul[1]/li/text()').extract())
        item['short_desc'] = response.selector.xpath('//div[@id="product-heading"]/h1/span[@itemprop="name"]/text()').extract()[0]
        item['product_link'] = response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]

        item['cat_1'] = ""
        item['cat_2'] = ""
        item['cat_3'] = ""
        item['cat_code'] = ""

        item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]
        item['date_last_updated'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

        item['image_urls'] = ""
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        try:
            item['imglink_1'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[1]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_1'] = ""

        try:
            item['imglink_2'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[2]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_2'] = ""

        try:
            item['imglink_3'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[3]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_3'] = ""

        try:
            item['imglink_4'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[4]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_4'] = ""

        try:
            item['imglink_5'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[5]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_5'] = ""

        try:
            item['imglink_6'] = response.selector.xpath('//div[@id="expanded-image-container"]/ul/li[6]/a[@class="lgImageLink"]/@href').extract()
        except IndexError:
            item['imglink_6'] = ""

        item['mcat_1'] = ""
        item['mcat_2'] = ""
        item['mcat_3'] = ""
        item['mcat_4'] = ""
        item['mcat_5'] = ""
        item['mcat_code'] = ""

        item['merchant'] = "The Outnet"
        item['merchant_id']  = "5BIJ2J"
        item['merchant_prod_id'] = response.selector.xpath('//li[@id="details-section"]/ul/li/div[@class="tab-details translateSection"]/p[last()]/text()').extract()[0][-6:]

        item['is_available'] = 'True' #BOOLEAN
        item['currency'] = response.selector.xpath('//div[@id="product-info"]/@data-currency').extract()[0]
        item['currency_symbol'] = response.selector.xpath('//div[@class="prices-all"]/div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()[0][0]

        try:
            if (int(float(response.selector.xpath('//div[@class="prices-all"]/div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//div[@class="prices-all"]/div[@class="price-info"]/div[@class="price-original"]/text()').extract()[0][response.selector.xpath('//div[@class="prices-all"]/div[@class="price-info"]/div[@class="price-original"]/text()').extract()[0].find('price')+7:]))):
                orig = int(float(response.selector.xpath('//div[@class="prices-all"]/div[@class="price-info"]/div[@class="price-original"]/text()').extract()[0][response.selector.xpath('//div[@class="prices-all"]/div[@class="price-info"]/div[@class="price-original"]/text()').extract()[0].find('price')+7:]))
                sale = int(float(response.selector.xpath('//div[@class="prices-all"]/div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()[0][1:]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
                item['on_sale'] = 'True' #BOOLEAN
            else:
                item['price_orig'] = int(float(response.selector.xpath('//div[@class="prices-all"]/div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
                item['on_sale'] = 'False'
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="prices-all"]/div[@itemprop="offers"]/span[@itemprop="price"]/text()').extract()[0][1:]))
            item['price'] = item['price_orig']
            item['on_sale'] = 'False' #BOOLEAN

        item['primary_color'] = ""

        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)

        yield item