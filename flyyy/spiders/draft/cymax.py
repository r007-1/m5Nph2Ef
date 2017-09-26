#https://www.cymax.com/sitemap.xml

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
#import js2xml, js2xml.jsonlike

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

class Cymax(scrapy.Spider):
    name = "cymax"
    allowed_domains = ["cymax.com"]
    is_test_run = False
    is_run = True
start_urls = []
if (is_run):
    sitemap_index = "https://www.cymax.com/sitemap.xml"
    sitemaps = []
    sitemap_tags = bs(requests.get(sitemap_index).text, "lxml").find_all("sitemap")
    for st in sitemap_tags:
        t = st.findNext("loc").text
        sitemaps.append(t)
for sitemap in sitemaps:
    tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
    for tag in tags:
        url = tag.findNext("loc").text
        if '/products/' in url:
            start_urls.append(url)
        if is_test_run:
            start_urls = start_urls[100:1000]
    start_urls = list(np.unique(start_urls))
    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)

        item = NuyolkItem()
        item['is_available'] = True
        item['affiliate_partner'] = "viglink"

        item['prod_id'] = str(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.url

        item['merchant'] = "Belk"
        item['merchant_prod_id'] = response.url.split("/")[-1].replace(".html", "")
        #item['upc'] ##TODO
        item['merchant_id'] = "IXR49N"

        try:
            item['brand'] = response.selector.xpath('//*[@itemprop="brand"]/text()').extract()[0]
        except:
            item['brand'] = ""
        item['short_desc'] = response.selector.xpath('//*[@class="brand-name"]/text()').extract()[0].strip()
        ld = response.selector.xpath('//meta[@name="description"]/@content').extract()
        ld.extend(response.selector.xpath('//ul[@class="copyline"]/li/text()').extract())
        skipwords = ["clean", "instructions", "cm", "wash", "in.", "inch", "size", "mm ", "size"]
        for w in skipwords:
            ld = list(np.array(ld)[np.array([w not in x for x in ld])])
        item['long_desc'] = " | ".join(ld).strip()
        item['primary_color'] = "" #later

        item['currency'] = response.selector.xpath('//meta[@itemprop="priceCurrency"]/@content').extract()[0]
        if (item['currency'] == 'USD'):
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?' ##TODO

        #If item is on sale,
        #[4:].replace(",", "")
        try:
            item['price_sale'] = int(float(response.selector.xpath("//*[@class='price-sales']/span/text()").extract()[0].replace(",", "")))
            item['price_orig'] = int(float(response.selector.xpath("//*[@class='price-standard']/text()").extract()[0].replace("Orig. $", "").replace(",", "")))
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
            item['on_sale'] = True
        except:
            try:
                item['price_orig'] = int(float(response.selector.xpath("//*[@class='standardprice']/input/@value").extract()[0].replace(",", "")))
            except:
                try:
                    item['price_orig'] = int(float(response.selector.xpath("//*[@class='standardprice']/span/text()").extract()[0].replace(",", "")))
                except:
                    print("??? SKIPPED!")
                    return
            item['price'] = item['price_orig']
            item['price_sale'] = item['price_orig']
            item['price_perc_discount'] = 0
            item['on_sale'] = False

        item['image_urls'] = response.selector.xpath('//div[@class="product-thumbnails"]//li/a/@href').extract()
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

        mcats = response.xpath('//script[contains(., "var utag_data")]/text()').re('product_category\"\: \[([^]]+)\]')[0].strip().replace('"', "")
        mcats = mcats.split(" > ")

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