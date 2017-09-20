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
import numpy as np
import numpy


class HBX(scrapy.Spider):
    name = "hbx"
    allowed_domains = ["hbx.com"]

    is_test_run = False
    is_run = False

    start_urls = []

    if (is_run):
        sitemap_index = "https://hbx.com/sitemap.xml"
        sitemaps = []

        sitemap_tags = bs(requests.get(sitemap_index).text, "lxml").find_all("sitemap")
        for st in sitemap_tags:
            sitemaps.append(st.findNext("loc").text)

        for sitemap in sitemaps:
            tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
            for tag in tags:
                start_urls.append(tag.findNext("loc").text)

        if is_test_run:
            start_urls = start_urls[0:10]

    start_urls = list(np.unique(start_urls))

    def parse(self, response):
        try:
            sold_out_msg = response.selector.xpath('//*[@class="sold-out-header"]/text()').extract()[0]
            print("SOLD OUT--SKIPPED!")
            return
        except:
            datetime = int(str(int(time.time()*100)))
            random.seed(1412112 + datetime)

            item = NuyolkItem()
            item['is_available'] = True
            item['affiliate_partner'] = "viglink"

            item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999)))
            item['product_link'] = response.selector.xpath('/html/head/meta[23]/@content').extract()[0]

            item['merchant'] = "HBX"
            item['merchant_prod_id'] = response.selector.xpath('//*[@id="product-summary"]/@data-id').extract()[0] #skipped
            item['merchant_id'] = "70856L"

            item['brand'] = response.selector.xpath('//h1[@class="brand"]/text()').extract()[0]
            item['short_desc'] = response.selector.xpath('//h1[@class="brand"]/text()').extract()[0]
            ld = response.selector.xpath('.//*[@class="description"]/p/text()').extract()
            item['long_desc'] = " | ".join(ld).strip()
            item['primary_color'] = "" #later

            item['currency'] = response.selector.xpath('//*[@class="currency-dropdown"]/span/text()').extract()[0]
            if (item['currency'] == 'USD'):
                item['currency_symbol'] = '$'
            else:
                item['currency_symbol'] = '?'

            #If item is on sale,
            try:
                item['price_sale'] = int(float(response.selector.xpath("//span[@class='sale-price']/text()").extract()[0][4:].replace(",", "")))
                item['price_orig'] = int(float(response.selector.xpath("//span[@class='regular-price']/text()").extract()[0][4:].replace(",", "")))
                item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
                item['price'] = item['price_sale']
                item['on_sale'] = True
            except:
                item['price_orig'] = int(float(response.selector.xpath("//span[@class='regular-price']/text()").extract()[0][4:].replace(",", "")))
                item['price'] = item['price_orig']
                item['price_sale'] = item['price_orig']
                item['price_perc_discount'] = 0
                item['on_sale'] = False

            item['image_urls'] = response.selector.xpath('.//ul[@class="slides"]/li/img/@src').extract()
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

            mcats = response.selector.xpath('.//ol[contains(@class, "breadcrumb") and contains(@class, "hidden-xs")]/li/a/text()').extract()
            mcats = [mc.strip() for mc in mcats]
            item['mcat_code'] = ""
            item['image_urls'] = ""

            for i in range(0, 5):
                attr = 'mcat_' + str(i + 1)
                try:
                    if i == len(mcats) - 1:
                        item[attr] = ""
                    elif i == 0:
                        if 'women' in response.url:
                            item[attr] = 'Women'
                        else:
                            item[attr] = 'Men'
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