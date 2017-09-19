from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import numpy
import numpy as np
import math
import csv
import re
import os

class Asos(scrapy.Spider):
    name = "asos-us"
    allowed_domains = ["us.asos.com"]

    is_test_run = False
    is_run = False
    max_cache_days = 3

    start_urls = []
    brand_urls = []

    if (is_run):
        try:
            mtime = os.path.getmtime("cache/asos-us.csv")
        except OSError:
            mtime = 0
        last_modified_date = datetime.datetime.fromtimestamp(mtime)
        age = datetime.datetime.today()-last_modified_date
        if (age.days >= max_cache_days):
            read_from_cache = False
        else:
            read_from_cache = True

        if read_from_cache:
            with open("cache/asos-us.csv", 'r') as my_file:
                reader = csv.reader(my_file, delimiter=',')
                start_urls_cache = list(reader)[0]
            start_urls = start_urls_cache
            start_urls = list(set(start_urls))
        else:
            brand_dirs = ["http://us.asos.com/women/a-to-z-of-brands/cat/?cid=1340", "http://us.asos.com/men/a-to-z-of-brands/cat/?cid=1361"]
            for dir in brand_dirs:
                d = requests.get(dir).content
                d = html.fromstring(d)
                brand_urls.extend(d.xpath('.//div[@class="brand-letter"]//a/@href'))
        for brand in brand_urls:
            try:
                print(brand_urls.index(brand))
                brand = brand + "&pgesize=204"
                b = requests.get(brand).content
                b = html.fromstring(b)
                num_items = int(b.xpath('//*[@class="total-results"]/text()')[0].replace(',',''))
                num_pages = int(math.ceil(num_items/204.0))
                if num_pages > 1:
                    for pg in range(0, num_pages):
                        p = brand + "&pge=" + str(pg)
                        p = requests.get(p).content
                        p = html.fromstring(p)
                        start_urls.extend(p.xpath('.//li[contains(@class, "product-container") and contains(@class, "interactions")]/a[contains(@class, "product") and contains(@class, "product-link")]/@href'))
                else:
                    p = b
                    start_urls.extend(p.xpath(
                        './/li[contains(@class, "product-container") and contains(@class, "interactions")]/a[contains(@class, "product") and contains(@class, "product-link")]/@href'))
            except IndexError:
                print("Dead link!")

            ## TODO: Check for duplicates!!!

            ## Save prod urls somewhere
            last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
            try:
                os.remove("cache/asos-us.csv")
            except:
                pass
            with open("cache/asos-us.csv", 'wb') as file:
                wr = csv.writer(file)
                wr.writerow(start_urls)

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
        #item['brand'] = response.selector.xpath('//div[@id = "productTabs"]/div[@id="ctl00_ContentMainPage_brandInfoPanel"]/a[1]/strong/text()').extract()[0]
        item['brand'] = response.xpath('//title/text()').extract_first().split(' | ')[0]
        descs = response.selector.xpath('//div[@class="product-description"]/span//text()').extract()
        descs = list(filter(lambda a: a != '    ', descs))
        skipwords = ["clean", "instructions", "cm", "wash", "in.", "inch", "size", "mm ", "size"]
        for w in skipwords:
            descs = list(np.array(descs)[np.array([w not in x for x in descs])])
        item['long_desc'] = "".join(descs[0:3]) + " | " + " | ".join(descs[3:len(descs)])
        #item['long_desc'] = " | ".join(response.selector.xpath('//div[@id="ctl00_ContentMainPage_productInfoPanel"]/ul/li/text()').extract())
        #item['short_desc'] = response.selector.xpath('//div[@class="title"]/h1/span[@class="product_title"]/text()').extract()[0]
        item['short_desc'] = response.selector.xpath('//div[@class="product-hero"]//h1/text()').extract()[0]
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
            item['imglink_1'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[1]/img/@src').extract()[0]
        except IndexError:
            item['imglink_1'] = ""
        try:
            item['imglink_2'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[2]//img/@src').extract()[0]
            item['imglink_2'] = item['imglink_2'].replace("S$&wid=40", "XXL$&wid=513")
        except IndexError:
            item['imglink_2'] = ""
        try:
            item['imglink_3'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[3]//img/@src').extract()[0]
            item['imglink_3'] = item['imglink_3'].replace("S$&wid=40", "XXL$&wid=513")
        except IndexError:
            item['imglink_3'] = ""
        try:
            item['imglink_4'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[4]//img/@src').extract()[0]
            item['imglink_4'] = item['imglink_4'].replace("S$&wid=40", "XXL$&wid=513")
        except IndexError:
            item['imglink_4'] = ""
        try:
            item['imglink_5'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[5]//img/@src').extract()[0]
            item['imglink_5'] = item['imglink_5'].replace("S$&wid=40", "XXL$&wid=513")
        except IndexError:
            item['imglink_5'] = ""
        try:
            item['imglink_6'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[6]//img/@src').extract()[0]
            item['imglink_6'] = item['imglink_6'].replace("S$&wid=40", "XXL$&wid=513")
        except IndexError:
            item['imglink_6'] = ""
        mcats = response.selector.xpath('//*[@id="more-from"]/descendant::a/text()').extract()

        for i in range(0, 5):
            attr = 'mcat_' + str(i + 1)
            try:
                item[attr] = mcats[i]
            except:
                item[attr] = ""
        item['mcat_code'] = ""
        item['merchant'] = "ASOS US"
        item['merchant_id']  = "IU95X3"
        item['merchant_prod_id'] = str(response.selector.xpath('//*[@class="product-code"]//span/text()').extract()[0])
        item['is_available'] = True #BOOLEAN
        p = "\n".join(response.selector.xpath('//script[contains(., "current")]/text()').extract())
        item['currency'] = find_between(p, '"currency":"', '",')[0:3]
        if (item['currency'] == 'USD'):
            item['currency_symbol'] =  '$'
        else:
            item['currency_symbol'] = '?'
        item['price'] = int(float(find_between(p, '"current":', ",")))
        prev = float(find_between(p, '"previous":', ","))
        rrp = float(find_between(p, '"rrp":', ","))
        if (prev==0 and rrp==0):
            item['price_orig'] = item['price']
            item['price_sale'] = item['price']
            item['price_perc_discount'] = 0
            item['on_sale'] = False
        else:
            item['price_sale'] = item['price']
            if (prev > 0):
                item['price_orig'] = int(prev)
            elif (rrp > 0):
                item['price_orig'] = int(rrp)
            else:
                item['price_orig'] = int(0) ###TODO ???
            item['on_sale'] = True
            item['price_perc_discount'] = int(100-100*(item['price_sale']/item['price_orig']))
        item['primary_color'] = ""
        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)
        yield item