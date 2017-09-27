from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import math
import string
import csv
import numpy
import numpy as np
import os
#import js2xml, js2xml.jsonlike

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

class Society6(scrapy.Spider):
    name = "society6"
    allowed_domains = ["society6.com"]
    is_test_run = True
    is_run = False
    try:
        mt = os.path.getmtime("cache/society6_urls.csv")
        tn = time.time()
        days_old = (datetime.datetime(1,1,1) + datetime.timedelta(seconds=tn-mt)).day - 1
        if (days_old < 3):
            read_from_cache = True
        else:
            read_from_cache = False
    except:
        read_from_cache = False
    start_urls = []
    if (is_run):
        if (read_from_cache):
            with open("cache/society6_urls.csv", 'r') as my_file:
                reader = csv.reader(my_file, delimiter=',')
                my_list = list(reader)
                start_urls = my_list[0]
        else:
            sitemap_index = "https://society6.com/sitemap/index.xml"
            sitemaps = []
            sitemap_tags = bs(requests.get(sitemap_index).text, "lxml").find_all("sitemap")
            for st in sitemap_tags:
                t = st.findNext("loc").text
                if '/product/' in t:
                    sitemaps.append(t)
            for sitemap in sitemaps:
                print(sitemap)
                tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
                for tag in tags:
                    url = tag.findNext("loc").text
                    if '/product/' in url:
                        start_urls.append(url)
                print(len(start_urls))
        start_urls = list(np.unique(start_urls))
        if is_test_run:
            start_urls = start_urls[10000:10100]
        if (len(start_urls) > 250000):
            os.remove("cache/society6_urls.csv")
            with open("cache/society6_urls.csv", 'wb') as f:
                wr = csv.writer(f)
                wr.writerow(start_urls)
    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)

        item = NuyolkItem()
        item['is_available'] = True
        item['affiliate_partner'] = "viglink"

        item['prod_id'] = str(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.url

        item['merchant'] = "Society6"
        try:
            mpi = response.xpath('//script[contains(., "dataLayer = ")]/text()').re('\"id\"\:\"(.*)')[0]
            mpi = mpi.split("\"")[0]
            item['merchant_prod_id'] = mpi
        except:
            pass
        item['merchant_id'] = "7599C0"

        try:
            brand = response.selector.xpath('//*[@class="user-avatar"]/a/img/@alt').extract()[0]
            brand = brand.split(" (")[0].strip()
            item['brand'] = brand
        except:
            item['brand'] = ""
        sd = response.selector.xpath('//title/text()').extract()[0]
        sd = sd.split(" by ")[0].capitalize()
        item['short_desc'] = sd
        try:
            ld = [response.selector.xpath('//*[@id="about-the-art-description"]/text()').extract()[0].strip()]
        except:
            ld = []
        ld2 = response.selector.xpath('//*[@id="product-description"]//text()').extract()[0].strip().split(". ")
        ld2last = ld2[-1]
        ld2 = [x + "." for x in ld2[:-1]]
        ld2.append(ld2last)
        ld.extend(ld2)
        skipwords = ["clean", "instructions", "cm", "\" ", "wash", "in.", "inch", "size", "mm ", "size", "weighs", "lbs."]
        for w in skipwords:
            ld = list(np.array(ld)[np.array([w not in x for x in ld])])
        item['long_desc'] = " | ".join(ld).strip()
        item['primary_color'] = "" #later
        item['currency'] = response.selector.xpath('//meta[@property="og:price:currency"]/@content').extract()[0]
        if (item['currency'] == 'USD'):
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?' ##TODO

        #If item is on sale,
        #[4:].replace(",", "")
        try:
            #####TODO (cannot find products on sale)
            item['price_sale'] = int(float(response.selector.xpath('//meta[@property="og:price:sale"]/@content').extract()[0].replace(",", "")))
            item['price_orig'] = int(float(response.selector.xpath('//meta[@property="og:price:orig"]/@content').extract()[0].replace(",", "")))
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
            item['on_sale'] = True
        except:
            item['price_orig'] = int(float(response.selector.xpath('//meta[@property="og:price:amount"]/@content').extract()[0].replace(",", "")))
            item['price'] = item['price_orig']
            item['price_sale'] = item['price_orig']
            item['price_perc_discount'] = 0
            item['on_sale'] = False
        item['image_urls'] = response.selector.xpath('//*[@id="product-image-main"]//img/@src').extract()
        #response.selector.xpath('//*[@class="zoom masterTooltip"]/img/@src').extract() #new
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        for i in range(0,6):
            attr = 'imglink_' + str(i+1)
            try:
                item[attr] = item['image_urls'][i]
            except:
                item[attr] = ""

        mcats = response.selector.xpath('//*[@class="breadcrumb_v2"]//span/text()').extract()
        mcats = filter(lambda x: x != "/", mcats)
        mcats = mcats[1:-1]

        item['mcat_code'] = ""
        item['image_urls'] = ""

        for i in range(0, 5):
            attr = 'mcat_' + str(i + 1)
            try:
                if i == len(mcats) - 1:
                    item[attr] = ""
                else:
                    item[attr] = mcats[i]
            except:
                item[attr] = ""

        item['cat_code'] = ""
        item['cat_1'] = "" #deprecate
        item['cat_2'] = "" #deprecate
        item['cat_3'] = "" #deprecate

        t = [item['brand'], item['short_desc'], item['mcat_1'], mcats[1:], item['long_desc']]
        item['tags'] = " ".join(list(numpy.hstack(t)))

        item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
        item['date_last_updated'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))

        yield item