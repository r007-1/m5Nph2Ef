from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import numpy
import math
import csv
import numpy as np

class TheOutnet(scrapy.Spider):
    name = "theoutnet-us"
    allowed_domains = ["theoutnet.com"]
    is_test_run = False
    is_run = False
    start_urls = []
    if (is_run):
        sitemaps = []
        sitemap_main = ["https://www.theoutnet.com/en-US/sitemap.xml"]
        main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("url")
        for main_tag in main_tags:
            t = main_tag.findNext("loc").text
            if 'Product' in t:
                start_urls.append(t)
        if is_test_run:
            start_urls = start_urls[0:50]
    start_urls = list(np.unique(start_urls))
    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!

        item['affiliate_partner'] = "viglink"
        item['brand'] = response.selector.xpath('//div[@class="name-and-price"]//a/text()').extract()[0]

        ld = response.selector.xpath('//*[contains(@class, "size-and-fit") and contains(@class, "accordion-content")]/ul/li/text()').extract()[1:]
        skipwords = ["clean", "instructions", "cm", "wash", "in.", "inch", "size", "mm ", "size"]
        for w in skipwords:
            ld = list(np.array(ld)[np.array([w not in x for x in ld])])
        item['long_desc'] = " | ".join(ld).strip()

        item['short_desc'] = response.selector.xpath('//div[@class="name-and-price"]//span/text()').extract()[0]
        item['product_link'] = response.url

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

        imglinks = response.selector.xpath('.//*[@class="product-images"]//img/@data-src').extract()
        imglinks = [("https:" + img).replace("_m.jpg", "_xl.jpg") for img in imglinks]
        imglinks = list(set(imglinks))
        for i in range(0, 6):
            attr = 'imglink_' + str(i + 1)
            try:
                item[attr] = imglinks[i]
            except:
                item[attr] = ""

        mcats = response.selector.xpath('.//*[@class="header-breadcrumbs"]//a/text()').extract()[1:]

        for i in range(0, 5):
            attr = 'mcat_' + str(i + 1)
            try:
                item[attr] = mcats[i]
            except:
                item[attr] = ""

        item['mcat_code'] = ""

        item['merchant'] = "The Outnet US"
        item['merchant_id']  = "5BIJ2J"
        item['merchant_prod_id'] = response.selector.xpath('//*[contains(@class, "size-and-fit") and contains(@class, "accordion-content")]//p[last()]/text()').extract()[0][-6:]

        item['is_available'] = True
        item['currency'] = response.selector.xpath('//*[@id="product-container"]/@data-analytics-currency').extract()[0]
        if item['currency'] == 'USD':
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?'

        try:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="price-info"]/span[1]/text()').extract()[0][5:]))
            item['price'] = int(float(response.selector.xpath('//span[@class="exact-price"]/text()').extract()[0].strip()[1:]))
            item['price_sale'] = item['price']
            item['on_sale'] = True
            item['price_perc_discount'] = int(100-100*(item['price_sale']/(item['price_orig']*1.0)))
        except:
            item['price_orig'] = int(float(response.selector.xpath('//span[@class="exact-price"]/text()').extract()[0].strip()[1:]))
            item['price'] = item['price_orig']
            item['price_sale'] = item['price_orig']
            item['on_sale'] = False
            item['price_perc_discount'] = 0

        item['primary_color'] = ""


        t = [item['brand'], item['short_desc'], "Women", mcats, item['long_desc']]
        item['tags'] = " ".join(list(numpy.hstack(t)))

        yield item
