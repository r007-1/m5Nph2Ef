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

class Revolve(scrapy.Spider):
    name = "revolve"
    allowed_domains = ["revolve.com"]
    is_test = True
    is_run = True
    start_urls = []
    sitemaps = []
    if (is_run):
        sitemap_main = ["http://www.revolve.com/scripts/rev_sitemap/rev_sitemap_index.xml"]
        main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("url")
        for main_tag in main_tags:
           sitemaps.append(main_tag.findNext("loc").text)
        for sitemap in sitemaps:
            tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
            for tag in tags:
                prod_link = tag.findNext("loc").text
                if 'dp' in prod_link:
                    start_urls.append(prod_link)
        if (is_test):
            start_urls = start_urls[50:60]
    start_urls = list(np.unique(start_urls))
    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!
        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!
        item['affiliate_partner'] = "viglink"
        item['brand'] = response.selector.xpath('//meta[@name="twitter:data2"]/@content').extract()[0]
        ld = response.selector.xpath('//div[@class="product-details__content js-tabs__content js-tabs__content-active product-details__description"]/ul/li/text()').extract()
        if (len(ld)>=7):
            ld = ld[:7]
        ld = filter(lambda x: "Style No." not in x and " cm" not in x, ld)
        item['long_desc'] = " | ".join(ld)
        item['short_desc'] = response.selector.xpath('//*[@class="product-titles"]//h1/text()').extract()[0].strip()
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
            item['imglink_1'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[1]/@data-image').extract()[0]
        except IndexError:
            item['imglink_1'] = ""

        try:
            item['imglink_2'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[2]/@data-image').extract()[0]
        except IndexError:
            item['imglink_2'] = ""

        try:
            item['imglink_3'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[3]/@data-image').extract()[0]
        except IndexError:
            item['imglink_3'] = ""

        try:
            item['imglink_4'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[4]/@data-image').extract()[0]
        except IndexError:
            item['imglink_4'] = ""

        try:
            item['imglink_5'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[5]/@data-image').extract()[0]
        except IndexError:
            item['imglink_5'] = ""

        try:
            item['imglink_6'] = response.selector.xpath('//div[@id="js-primary-slideshow__pager"]/a[6]/@data-image').extract()[0]
        except IndexError:
            item['imglink_6'] = ""
        mcats = response.selector.xpath('//*[@class="pdp_lower_area"]/div[5]//li//text()').extract()[1:]
        mcats = [x.strip() for x in mcats]
        mcats = filter(lambda x: x != "" and x!= item['brand'] and "REVOLVE" not in x, mcats)
        for i in range(0, 5):
            attr = 'mcat_' + str(i + 1)
            try:
                if i == len(mcats) - 1:
                    item[attr] = ""
                else:
                    item[attr] = mcats[i]
            except:
                item[attr] = ""
        item['mcat_code'] = ""
        item['merchant'] = "REVOLVE"
        item['merchant_id']  = "HE3T6E"
        item['merchant_prod_id'] = response.selector.xpath('//input[@id="productCode"]/@value').extract()[0]
        item['is_available'] = True
        item['currency'] = "USD"
        item['currency'] = response.selector.xpath('//meta[@property="wanelo:product:price:currency"]/@content').extract()[0]
        if (item['currency'] == 'USD'):
            item['currency_symbol'] = '$'
        else:
            item['currency_symbol'] = '?' ##TODO
        try:
            sale = int(float(response.selector.xpath('//div[@class="prices__retail--strikethrough"]/preceding::div/text()').extract()[-1][2:].replace(',', '')))
            orig = int(float(response.selector.xpath('//div[@class="prices__retail--strikethrough"]//text()').extract()[0][2:].replace(',', '')))
            if (orig != sale):
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(float(sale)/float(orig)))
                item['price'] = item['price_sale']
                item['on_sale'] = True
            else:
                item['price_orig'] = orig
                item['price'] = item['price_orig']
                item['price_sale'] = item['price_orig']
                item['price_perc_discount'] = 0
                item['on_sale'] = False
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//meta[@itemprop="price"]/@content').extract()[0]))
            item['price'] = item['price_orig']
            item['price_sale'] = ""
            item['on_sale'] = False #BOOLEAN
            item['price_perc_discount'] = 0
        item['primary_color'] = ""
        t = [item['brand'], item['short_desc'], item['mcat_1'], mcats[1:], item['long_desc']]
        item['tags'] = " ".join(list(numpy.hstack(t)))
        yield item
