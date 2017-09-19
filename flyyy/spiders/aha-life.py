from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import numpy as np
import numpy
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import math
import csv
#coursera-dl -u myusername -p mypassword -d /my/coursera/courses/ algo-2012-001 ml-2012-002

class AHAlife(scrapy.Spider):
    name = "ahalife"
    allowed_domains = ["ahalife.com"]
    is_test_run = False
    is_run = True
    start_urls = []
    if (is_run):
        sitemaps = []
        sitemap_main = ["http://www.ahalife.com/sitemap.xml"]
        main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("url")
        for main_tag in main_tags:
           if 'product' in str(main_tag):
               start_urls.append(main_tag.findNext("loc").text)
        if is_test_run:
            start_urls = start_urls[0:10]
        start_urls = list(np.unique(start_urls))
    def parse(self, response):
        def find_between(s, first, last):
            try:
                start = s.index(first) + len(first)
                end = s.index(last, start)
                return s[start:end]
            except ValueError:
                return ""
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!
        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!
        item['affiliate_partner'] = "viglink"
        item['brand'] = response.selector.xpath('//a[@id="product-brand"]/text()').extract()[0]
        ld = [response.selector.xpath('//div[@id="details"]//span/text()').extract()[0]]
        ld.extend(response.selector.xpath('.//div[@id="productDetail-details"]//p/text()').extract())
        skipwords = ["clean", "instructions", "cm", "wash", "in.", "inch", "size", "mm ", "size"]
        for w in skipwords:
            ld = list(np.array(ld)[np.array([w not in x for x in ld])])

        item['long_desc'] = " | ".join(list(numpy.hstack(ld)))

        item['short_desc'] = response.selector.xpath('//h1[@class="heading1"]/text()').extract()[0]
        item['product_link'] = response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]
        item['cat_1'] = ""
        item['cat_2'] = ""
        item['cat_3'] = ""
        item['cat_code'] = ""
        item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
        item['date_last_updated'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
        item['image_urls'] = ""
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""
        try:
            item['imglink_1'] = response.selector.xpath('//ul[@id="carousel"]/li[1]/a/@href').extract()[0]
        except IndexError:
            item['imglink_1'] = ""
        try:
            item['imglink_2'] = response.selector.xpath('//ul[@id="carousel"]/li[2]/a/@href').extract()[0]
        except IndexError:
            item['imglink_2'] = ""
        try:
            item['imglink_3'] = response.selector.xpath('//ul[@id="carousel"]/li[3]/a/@href').extract()[0]
        except IndexError:
            item['imglink_3'] = ""
        try:
            item['imglink_4'] = response.selector.xpath('//ul[@id="carousel"]/li[4]/a/@href').extract()[0]
        except IndexError:
            item['imglink_4'] = ""
        try:
            item['imglink_5'] = response.selector.xpath('//ul[@id="carousel"]/li[5]/a/@href').extract()[0]
        except IndexError:
            item['imglink_5'] = ""
        try:
            item['imglink_6'] = response.selector.xpath('//ul[@id="carousel"]/li[6]/a/@href').extract()[0]
        except IndexError:
            item['imglink_6'] = ""

        mcats = response.selector.xpath('.//ul[@itemprop="category"]//li//a/text()').extract()

        for i in range(0, 5):
            attr = 'mcat_' + str(i + 1)
            try:
                item[attr] = mcats[i]
            except:
                item[attr] = ""

        item['mcat_code'] = ""
        item['merchant'] = "AHAlife"
        item['merchant_id']  = "SN4NSZ"
        item['merchant_prod_id'] = find_between(response.url,"/product/", "/")
        item['is_available'] = True
        item['currency'] = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract()[0]

        if (item['currency'] == 'USD'):
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?'

        item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-price sku-price"]/@data-base-price').extract()[0]))
        item['price'] = item['price_orig']
        item['price_sale'] = item['price_orig']
        item['on_sale'] = False #BOOLEAN
        item['price_perc_discount'] = 0
        item['primary_color'] = ""

        t = [item['brand'], item['short_desc'], item['mcat_1'], mcats[1:], item['long_desc']]
        item['tags'] = " ".join(list(numpy.hstack(t)))

        yield item
