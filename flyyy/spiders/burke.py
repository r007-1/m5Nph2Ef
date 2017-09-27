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

class Burke(scrapy.Spider):
    name = "burke"
    allowed_domains = ["burkedecor.com"]
    is_test_run = False
    is_run = False
    start_urls = []
    if (is_run):
        sitemap_index = "https://www.burkedecor.com/sitemap.xml"
        sitemaps = []
        sitemap_tags = bs(requests.get(sitemap_index).text, "lxml").find_all("sitemap")
        for st in sitemap_tags:
            t = st.findNext("loc").text
            if 'products' in t:
                sitemaps.append(t)
        for sitemap in sitemaps:
            tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
            for tag in tags:
                url = tag.findNext("loc").text
                if '/products/' in url:
                    start_urls.append(url)
        if (is_test_run):
            start_urls = start_urls[100:200]
    start_urls = list(np.unique(start_urls))
    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)
        item = NuyolkItem()
        item['is_available'] = True
        item['affiliate_partner'] = "viglink"
        item['prod_id'] = str(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.url
        item['merchant'] = "Burke Decor"
        try:
            item['merchant_prod_id'] = response.selector.xpath('//*[@class="product-status"]/text()').extract()[0].replace("SKU: ", "").strip()
        except:
            return
        #item['upc'] ##TODO
        item['merchant_id'] = "A82I78"
        try:
            item['brand'] = response.selector.xpath('//*[@class="product_meta"]//a/text()').extract()[0]
        except:
            item['brand'] = ""
        item['short_desc'] = response.selector.xpath('//*[@itemprop="name"]/@content').extract()[0]
        try:
            ld = [response.selector.xpath('//p[@itemprop="description"]/following::p/text()').extract()[0]]
            if ld==[u'\xa0']:
                ld = []
            ld2 = response.selector.xpath('//p[@itemprop="description"]/following::ul[1]//text()').extract()
            ld2 = filter(lambda x: "%" in x or "Finish" in x, ld2)
            ld.extend(ld2)
            skipwords = ["clean", "instructions", "cm", "wash", "in.", "inch", "size", "mm ", "size", "Weight", "Dimensions"]
            for w in skipwords:
                ld = list(np.array(ld)[np.array([w not in x for x in ld])])
            item['long_desc'] = " | ".join(ld).strip()
        except:
            # out of stock
            return
        item['primary_color'] = "" #later
        item['currency'] = response.selector.xpath('//meta[@itemprop="priceCurrency"]/@content').extract()[0]
        if (item['currency'] == 'USD'):
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?' ##TODO
        #If item is on sale,
        #[4:].replace(",", "")
        try:
            item['price_sale'] = int(float(response.selector.xpath('//*[@id="ProductPrice"]/text()').extract()[0].strip()[1:]))
            item['price_orig'] = int(float(response.selector.xpath('//*[@id="ComparePrice"]/text()').extract()[0].strip()[1:].replace(",","")))
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
            item['on_sale'] = True
        except:
            item['price_orig'] = int(float(response.selector.xpath('//*[@id="ProductPrice"]/text()').extract()[0].strip()[1:].replace(",","")))
            item['price'] = item['price_orig']
            item['price_sale'] = item['price_orig']
            item['price_perc_discount'] = 0
            item['on_sale'] = False
        item['image_urls'] = response.selector.xpath('//*[@class="product-media"]//img//@src').extract()
        item['image_urls'] = ['http:' + x.split('?v=', 1)[0] for x in item['image_urls']]
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
        mcats = response.xpath('//script[contains(., "fbq(")]/text()').re('content_category\: \'([^]]+)')
        mcats = mcats[0].split(",")[0]
        mcats = mcats.split(" > ")
        mcats = filter(lambda x: "All" not in x and "New" not in x and "$" not in x and item['brand'] not in x and "Sale" not in x, mcats)
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