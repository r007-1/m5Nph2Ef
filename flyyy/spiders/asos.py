from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime
import pandas

class Asos(scrapy.Spider):
    name = "asos-us"
    allowed_domains = ["asos.com"]
    start_urls = []
    sitemaps = []

    sitemap_main = ["http://us.asos.com/sitemap.ashx"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
        sitemaps.append(main_tag.findNext("loc").text)

    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            prod_link = tag.findNext("loc").text
            if '?iid=' in prod_link:
                start_urls.append(prod_link)
    start_urls = start_urls[0:25]

    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!

        item['affiliate_partner'] = "viglink"
        item['brand'] = response.selector.xpath('//div[@id = "productTabs"]/div[@id="ctl00_ContentMainPage_brandInfoPanel"]/a[1]/strong/text()').extract()[0]
        item['long_desc'] = " | ".join(response.selector.xpath('//div[@id="ctl00_ContentMainPage_productInfoPanel"]/ul/li/text()').extract())
        item['short_desc'] = response.selector.xpath('//div[@class="title"]/h1/span[@class="product_title"]/text()').extract()[0]
        item['product_link'] = response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]

        item['cat_1'] = ""
        item['cat_2'] = ""
        item['cat_3'] = ""
        item['cat_code'] = ""

        item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]
        item['date_last_updated'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

        item['image_urls'] = ""
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        try:
            item['imglink_1'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage1"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_1'] = ""

        try:
            item['imglink_2'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage2"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_2'] = ""

        try:
            item['imglink_3'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage3"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_3'] = ""

        try:
            item['imglink_4'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage4"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_4'] = ""

        try:
            item['imglink_5'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage5"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_5'] = ""

        try:
            item['imglink_6'] = response.selector.xpath('//div[@id="ctl00_ContentMainPage_mainImage6"]/img/@src').extract()[0]
        except IndexError:
            item['imglink_6'] = ""

        item['mcat_1'] = ""
        item['mcat_2'] = ""
        item['mcat_3'] = ""
        item['mcat_4'] = ""
        item['mcat_5'] = ""
        item['mcat_code'] = ""

        item['merchant'] = "ASOS US"
        item['merchant_id']  = "IU95X3"
        item['merchant_prod_id'] = response.selector.xpath('//span[@class="productcode"]/text()').extract()[0]

        item['is_available'] = True #BOOLEAN
        item['currency'] = response.selector.xpath('//div[@class="currency-list"]/select/option[@selected="selected"]/text()').extract()[0][-3:]
        item['currency_symbol'] = response.selector.xpath('//div[@class="currency-list"]/select/option[@selected="selected"]/text()').extract()[0][0:response.selector.xpath('//div[@class="currency-list"]/select/option[@selected="selected"]/text()').extract()[0].find(" ")]

        try:
            if (int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPreviousPrice"]/text()').extract()[0][1:]))):
                orig = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
                sale = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPreviousPrice"]/text()').extract()[0][1:]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
                item['on_sale'] = True #BOOLEAN
            else:
                item['price_orig'] = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
            item['price'] = item['price_orig']
            item['on_sale'] = False #BOOLEAN

        item['primary_color'] = ""

        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)

        yield item