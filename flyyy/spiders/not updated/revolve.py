from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime

class Revolve(scrapy.Spider):
    name = "revolve"
    allowed_domains = ["revolve.com"]
    start_urls = []
    sitemaps = []
    '''
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

    start_urls = start_urls[0:10]
    '''
    def parse(self, response):
        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!

        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!

        item['affiliate_partner'] = "viglink"
        item['brand'] = "REVOLVE"
        item['long_desc'] = " | ".join(response.selector.xpath('//div[@class="product-details__content js-tabs__content js-tabs__content-active product-details__description"]/ul/li/text()').extract())
        item['short_desc'] = response.selector.xpath('//h1[@class="product-titles__name product-titles__name--long u-margin-b--none u-margin-t--lg"]/text()').extract()[0].strip()
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

        item['mcat_1'] = ""
        item['mcat_2'] = ""
        item['mcat_3'] = ""
        item['mcat_4'] = ""
        item['mcat_5'] = ""
        item['mcat_code'] = ""

        item['merchant'] = "REVOLVE"
        item['merchant_id']  = "HE3T6E"
        item['merchant_prod_id'] = response.selector.xpath('//input[@id="productCode"]/@value').extract()[0]

        item['is_available'] = 'True' #BOOLEAN
        item['currency'] = "USD"
        item['currency_symbol'] = "$"

        try:
            if (int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__retail-strikethrough"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__markdown u-margin-r--xs"]/text()').extract()[0][1:]))):
                orig = int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__retail-strikethrough"]/text()').extract()[0][1:]))
                sale = int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__markdown u-margin-r--xs"]/text()').extract()[0][1:]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
                item['on_sale'] = 'True' #BOOLEAN
            else:
                item['price_orig'] = int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__retail-strikethrough"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
                item['price_sale'] = ""
                item['on_sale'] = 'False'
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="prices prices--md block block--lg"]/span[@class="prices__retail"]/text()').extract()[0][1:]))
            item['price'] = item['price_orig']
            item['price_sale'] = ""
            item['on_sale'] = 'False' #BOOLEAN

        item['primary_color'] = ""

        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)

        yield item
