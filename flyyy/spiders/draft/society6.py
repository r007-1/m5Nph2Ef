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

class Society6(scrapy.Spider):
    name = "society6"
    allowed_domains = ["society6.com"]
    is_test_run = True
    is_run = True
    read_from_cache = True
    start_urls = []
    if (is_run):
        if (read_from_cache):
            f = open('cache/society6_links.csv')
            start_urls = f.readlines()
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
        if is_test_run:
            start_urls = start_urls[10000:10100]
    if (len(start_urls) > 250000):
        csv.writer(start_urls)
    start_urls = list(np.unique(start_urls))
    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)

        item = NuyolkItem()
        item['is_available'] = True
        item['affiliate_partner'] = "viglink"

        item['prod_id'] = str(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.url

        item['merchant'] = "Lamps Plus"
        try:
            item['merchant_prod_id'] = response.selector.xpath('//*[@id="pdProdSku"]/text()').extract()[0].replace('- Style # ', '')
        except:
            pass
        item['merchant_id'] = "7599C0"

        try:
            item['brand'] = response.selector.xpath('//*[@id="pnlBrand"]/@content').extract()[0]
        except:
            item['brand'] = ""
        item['short_desc'] = response.selector.xpath('//*[@id="h1ProductName"]/text()').extract()[0].strip()

        ld = [response.selector.xpath('//*[@id="pdKeySentence"]/text()').extract()[0].strip()]
        ld2 = [response.selector.xpath('//p[@itemprop="description"]/text()').extract()[0].strip()]
        ld3 = response.selector.xpath('//*[@id="pdDescBullets"]/li/text()').extract()
        ld.extend(ld2)
        ld.extend(ld3)
        skipwords = ["clean", "instructions", "cm", "\" ", "wash", "in.", "inch", "size", "mm ", "size", "weighs", "lbs."]
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
            item['price_sale'] = int(float(response.selector.xpath("//*[@itemprop='lowPrice']/@content").extract()[0].replace(",", "")))
            item['price_orig'] = int(float(response.selector.xpath("//*[@itemprop='highPrice']/@content").extract()[0].replace(",", "")))
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
            item['on_sale'] = True
        except:
            item['price_orig'] = int(float(response.selector.xpath("//*[@itemprop='price']/@content").extract()[0].replace(",", "")))
            item['price'] = item['price_orig']
            item['price_sale'] = item['price_orig']
            item['price_perc_discount'] = 0
            item['on_sale'] = False

        imgs = response.selector.xpath('//*[@id="pdAddlImgs"]//img/@src').extract()
        item['image_urls'] = [x.replace(find_between(x, 'fpx?', 'fmt=jpeg'), "") for x in imgs]
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

        mcats = response.selector.xpath('//*[@id="divBreadCrumb"]//text()').extract()
        mcats = [x.strip() for x in mcats]
        mcats = filter(lambda x: x != "" and x != "|", mcats)
        mcats = mcats[1:-2]

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