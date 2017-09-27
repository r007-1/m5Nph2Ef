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
        ##TODO remove manufacturer links http://www.lampsplus.com/products/bathroom-lighting/finish_chrome/color_gray/manufacturer_hinkley/
        #http://www.lampsplus.com/products/cabinets-and-storage/finish_pecan/usage_living-@-family-room/type_bookshelves/
        #http://www.lampsplus.com/products/cabinets-and-storage/finish_pecan/usage_office/
        #http://www.lampsplus.com/products/cabinets-and-storage/style_mid@century/finish_chrome/color_white-@-ivory/
        #http: // www.lampsplus.com / products / cabinets - and -storage/style_rustic-@-lodge / usage_office / type_bookshelves /
        #http://www.lampsplus.com/products/cabinets-and-storage/style_traditional/finish_cherry/manufacturer_howard-miller/
class LampsPlus(scrapy.Spider):
    name = "lamps_plus"
    allowed_domains = ["lampsplus.com"]
    is_test_run = False
    is_run = True
    start_urls = []
    if (is_run):
        sitemap_index = "http://www.lampsplus.com/sitemap-index.xml"
        sitemaps = []
        sitemap_tags = bs(requests.get(sitemap_index).text, "lxml").find_all("sitemap")
        for st in sitemap_tags:
            t = st.findNext("loc").text
            if 'products/' in t:
                sitemaps.append(t)
        for sitemap in sitemaps:
            tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
            for tag in tags:
                url = tag.findNext("loc").text
                vp = "usage_" in url or "manufacturer_" in url or "finish_" in url or "color_" in url or "style_" in url or "type_" in url
                if (not vp):
                    start_urls.append(url)
    start_urls = list(np.unique(start_urls))
    if is_test_run:
        start_urls = start_urls[1000:1100]
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
            return
        item['merchant_id'] = "P2B2J5"

        try:
            item['brand'] = response.selector.xpath('//*[@id="pnlBrand"]/@content').extract()[0]
        except:
            item['brand'] = ""

        try:
            item['short_desc'] = response.selector.xpath('//*[@id="h1ProductName"]/text()').extract()[0].strip()
        except:
            return

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