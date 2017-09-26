from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import math
import csv
import numpy
import numpy as np


#start 06/02/2016 03:18:22
#end 2016-02-06 09:48:24
#24844 products

#### CRAWLER BLOCKED

class Barneys(scrapy.Spider):
    name = "barneys"
    allowed_domains = ["barneys.com"]
start_urls = []

sm1 = "http://www.barneys.com/product-sitemap_bny.xml"
sm2 = "http://www.barneys.com/product-sitemap_bny1.xml"

sitemapTags1 = bs(requests.get(sm1).text, "lxml").find_all("url")
sitemapTags2 = bs(requests.get(sm2).text, "lxml").find_all("url")

for sitemap1 in sitemapTags1:
    start_urls.append(sitemap1.findNext("loc").text)
for sitemap2 in sitemapTags2:
    start_urls.append(sitemap2.findNext("loc").text)

    def parse(self, response):

        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)

        item = NuyolkItem()

        item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.selector.xpath('/html/head/meta[12]/@content').extract()[0]

        item['merchant_prod_id'] = response.selector.xpath('/html/head/meta[17]/@content').extract()[0]
        item['merchant_id'] = "70856L"

        item['brand'] = response.selector.xpath('//h1[@class="brand"]/a/text()').extract()[0]
        item['short_desc'] = response.selector.xpath('//h1[@class="product-name"]/text()').extract()[0]
        item['long_desc'] = response.selector.xpath('/html/head/meta[4]/@content').extract()[0]
        item['primary_color'] = "" #later

        item['currency'] = response.selector.xpath('/html/head/meta[19]/@content').extract()[0]

        #If item is on sale,
        if (response.selector.xpath("//span[@class='price-standard']/text()").extract() != []):
            item['price_orig'] = response.selector.xpath("//span[@class='price-standard']/text()").extract()[0][1:]
            item['price_sale'] = response.selector.xpath("//span[@class='price-sales']/text()").extract()[0][1:]
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
        else:
            item['price_orig'] = response.selector.xpath("//span[@class='price-sales']/text()").extract()[0][1:]
            item['price'] = item['price_orig']

        item['image_urls'] = response.selector.xpath('//*[@class="zoom masterTooltip"]/img/@src').extract() #new
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        #new
        item['mcats'] = response.selector.xpath('//*[@id="main"]/div/div/ol/li/a/text()').extract()

        for i in range(0, len(item['mcats'])):
            attr = 'mcat_' + str(i+1)
            item[attr] = item['mcats'][i]

        item['cat_code'] = ""
        item['cat_1'] = "" #deprecate
        item['cat_2'] = "" #deprecate
        item['cat_3'] = "" #deprecate

        tags = [str(response.selector.xpath('//h1[@class="brand"]/a/text()').extract()[0]), str(response.selector.xpath('//h1[@class="product-name"]/text()').extract()[0]), str(" ".join(item['mcats'])), str(response.selector.xpath('/html/head/meta[4]/@content').extract()[0])]
        item['tags'] = " ".join(tags)

        item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

        yield item
