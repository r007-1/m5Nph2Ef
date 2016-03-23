from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime

class SaksFifthAvenue(scrapy.Spider):
    name = "saks-fifth-avenue"
    allowed_domains = ["saksfifthavenue.com"]
    start_urls = []
    sitemaps = []

    sitemap_main = ["http://www.saksfifthavenue.com/sitemap/index.xml"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
        if 'detail' in main_tag:
            sitemaps.append(main_tag.findNext("loc").text)

    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            prod_link = tag.findNext("loc").text
            if 'PRODUCT' in prod_link:
                start_urls.append(prod_link)


    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!

        item['affiliate_partner'] = "viglink"
        item['brand'] = "Saks Fifth Avenue"
        item['long_desc'] = " | ".join(response.selector.xpath('//section[@class="product-description"]/div/text()').extract().append(response.selector.xpath('//section[@class="product-description"]/div/ul/li/text()').extract()))
        item['short_desc'] = response.selector.xpath('//h1[@class="product-overview__short-description"]/text()').extract()[0]
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
            item['imglink_1'] = "http://s7d9.scene7.com/is/image/saks/" + response.selector.xpath('//h4[@class="product-overview__product-code"]/text()').extract()[0]
        except IndexError:
            item['imglink_1'] = ""

        try:
            item['imglink_2'] = "http://s7d9.scene7.com/is/image/saks/" + response.selector.xpath('//h4[@class="product-overview__product-code"]/text()').extract()[0] + "_ASTL"
        except IndexError:
            item['imglink_2'] = ""

        try:
            item['imglink_3'] = "http://s7d9.scene7.com/is/image/saks/" + response.selector.xpath('//h4[@class="product-overview__product-code"]/text()').extract()[0] + "_A1"
        except IndexError:
            item['imglink_3'] = ""

        try:
            item['imglink_4'] = "http://s7d9.scene7.com/is/image/saks/" + response.selector.xpath('//h4[@class="product-overview__product-code"]/text()').extract()[0] + "_A2"
        except IndexError:
            item['imglink_4'] = ""

        try:
            item['imglink_5'] = ""
        except IndexError:
            item['imglink_5'] = ""

        try:
            item['imglink_6'] = ""
        except IndexError:
            item['imglink_6'] = ""

        item['mcat_1'] = ""
        item['mcat_2'] = ""
        item['mcat_3'] = ""
        item['mcat_4'] = ""
        item['mcat_5'] = ""
        item['mcat_code'] = ""

        item['merchant'] = "Saks Fifth Avenue"
        item['merchant_id']  = "90NZ70"
        item['merchant_prod_id'] = response.selector.xpath('//h4[@class="product-overview__product-code"]/text()').extract()[0]

        item['is_available'] = 'True' #BOOLEAN
        item['currency'] = "USD"
        item['currency_symbol'] = "$"

        try:
            if (int(float(response.selector.xpath('//div[@itemprop="offers"]/dl[1]/dd[@class="product-pricing__price"]/span[last()]/text()').extract()[0])) != int(float(response.selector.xpath('//div[@itemprop="offers"]/dl[1]/dd[@class="product-pricing__price"]/span[last()]/text()').extract()[0]))):
                orig = int(float(response.selector.xpath('//div[@itemprop="offers"]/dl[1]/dd[@class="product-pricing__price"]/span[last()]/text()').extract()[0]))
                sale = int(float(response.selector.xpath('//div[@itemprop="offers"]/dl[2]/dd[@class="product-pricing__price"]/span[last()]/text()').extract()[0]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
                item['on_sale'] = 'True' #BOOLEAN
            else:
                item['price_orig'] = int(float(response.selector.xpath('//dd[@class="product-pricing__price"]/span[@itemprop="price"]/text()').extract()[0]))
                item['price'] = item['price_orig']
                item['price_sale'] = ""
                item['on_sale'] = 'False'
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//dd[@class="product-pricing__price"]/span[@itemprop="price"]/text()').extract()[0]))
            item['price'] = item['price_orig']
            item['price_sale'] = ""
            item['on_sale'] = 'False' #BOOLEAN

        item['primary_color'] = ""

        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)

        yield item
