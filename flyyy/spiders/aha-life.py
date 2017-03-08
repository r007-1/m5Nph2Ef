from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime

class AHAlife(scrapy.Spider):
    name = "aha-life"
    allowed_domains = ["ahalife.com"]
    start_urls = []
    sitemaps = []
    sitemap_main = ["http://www.ahalife.com/sitemap.xml"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
        if 'product' in main_tag:
            sitemaps.append(main_tag.findNext("loc").text)
    start_urls = sitemaps
    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!
        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!
        item['affiliate_partner'] = "viglink"
        item['brand'] = "AHAlife"
        item['long_desc'] = response.selector.xpath('//div[@itemprop="description"]/p[2]/text()').extract()[0]
        item['short_desc'] = response.selector.xpath('//h1[@class="heading1"]/text()').extract()[0]
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
            item['imglink_1'] = response.selector.xpath('//ul[@id="carousel"]/li[1]/a/@href').extract()[0]
        except IndexError:
            item['imglink_1'] = ""
        try:
            item['imglink_2'] = response.selector.xpath('//ul[@id="carousel"]/li[2]/a/@href').extract()[0]
        except IndexError:
            item['imglink_2'] = ""
        try:
            item['imglink_3'] = response.selector.xpath('//ul[@id="carousel"]/li[3]/a/@href').extract()[0]
        except IndexError:
            item['imglink_3'] = ""
        try:
            item['imglink_4'] = response.selector.xpath('//ul[@id="carousel"]/li[4]/a/@href').extract()[0]
        except IndexError:
            item['imglink_4'] = ""
        try:
            item['imglink_5'] = response.selector.xpath('//ul[@id="carousel"]/li[5]/a/@href').extract()[0]
        except IndexError:
            item['imglink_5'] = ""
        try:
            item['imglink_6'] = response.selector.xpath('//ul[@id="carousel"]/li[6]/a/@href').extract()[0]
        except IndexError:
            item['imglink_6'] = ""
        item['mcat_1'] = ""
        item['mcat_2'] = ""
        item['mcat_3'] = ""
        item['mcat_4'] = ""
        item['mcat_5'] = ""
        item['mcat_code'] = ""
        item['merchant'] = "AHAlife"
        item['merchant_id']  = "SN4NSZ"
        item['merchant_prod_id'] = response.selector.xpath('//div[@class="shipping-info"]/ul[@class="details-sections"]/li[2]/span/text()').extract()[0]
        item['is_available'] = 'True' #BOOLEAN
        item['currency'] = 'USD'
        item['currency_symbol'] = '$'
        item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-price sku-price"]/@data-base-price').extract()[0]))
        item['price'] = item['price_orig']
        item['price_sale'] = ""
        item['on_sale'] = 'False' #BOOLEAN
        item['primary_color'] = ""
        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)
        yield item
