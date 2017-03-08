from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import random
import datetime

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
                start_urls.append(prod_link[0:prod_link.find("&mporgp")])
    #s = start_urls
    start_urls = start_urls[86850:]
    def parse(self, response):
        def find_between(s, first, last):
            try:
                start = s.index(first) + len(first)
                end = s.index(last, start)
                return s[start:end]
            except ValueError:
                return ""

        datetime = int(str(int(time.time()*100))) #Don't change!
        random.seed(1412112 + datetime) #Don't change!
        item = NuyolkItem() #Don't change!
        item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!
        item['affiliate_partner'] = "viglink"
        #item['brand'] = response.selector.xpath('//div[@id = "productTabs"]/div[@id="ctl00_ContentMainPage_brandInfoPanel"]/a[1]/strong/text()').extract()[0]
        item['brand'] = response.xpath('//title/text()').extract_first().split(' | ')[0]
        descs = response.selector.xpath('//div[@class="product-description"]/span//text()').extract()
        descs = list(filter(lambda a: a != '    ', descs))
        item['long_desc'] = "".join(descs[0:3]) + " | " + " | ".join(descs[3:len(descs)])
        #item['long_desc'] = " | ".join(response.selector.xpath('//div[@id="ctl00_ContentMainPage_productInfoPanel"]/ul/li/text()').extract())
        #item['short_desc'] = response.selector.xpath('//div[@class="title"]/h1/span[@class="product_title"]/text()').extract()[0]
        item['short_desc'] = response.selector.xpath('//div[@class="product-hero"]//h1/text()').extract()[0]
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
            item['imglink_1'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[1]/img/@src').extract()[0]
        except IndexError:
            item['imglink_1'] = ""
        try:
            item['imglink_2'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[2]//img/@src').extract()[0]
        except IndexError:
            item['imglink_2'] = ""
        try:
            item['imglink_3'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[3]//img/@src').extract()[0]
        except IndexError:
            item['imglink_3'] = ""
        try:
            item['imglink_4'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[4]//img/@src').extract()[0]
        except IndexError:
            item['imglink_4'] = ""
        try:
            item['imglink_5'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[5]//img/@src').extract()[0]
        except IndexError:
            item['imglink_5'] = ""
        try:
            item['imglink_6'] = response.selector.xpath('//div[@class="product-gallery"]//ul/li[6]//img/@src').extract()[0]
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
        item['merchant_prod_id'] = response.selector.xpath('//*[@class="product-code"]//span/text()').extract()[0]
        item['is_available'] = 1 #BOOLEAN
        p = "\n".join(response.selector.xpath('//script[contains(., "current")]/text()').extract())
        item['currency'] = find_between(p, '"currency":"', '",')
        item['currency_symbol'] = '$' ##improve later
        item['price'] = float(find_between(p, '"current":', ","))
        prev = float(find_between(p, '"previous":', ","))
        rrp = prev = float(find_between(p, '"rrp":', ","))
        if (prev==0 and rrp==0):
            item['price_orig'] = item['price']
            item['price_sale'] = item['price']
        else:
            item['price_sale'] = item['price']
            if (prev > 0):
                item['price_orig'] = prev
            elif (rrp > 0):
                item['price_orig'] = rrp
        '''
        try:
            if (int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPreviousPrice"]/text()').extract()[0][1:]))):
                orig = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
                sale = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPreviousPrice"]/text()').extract()[0][1:]))
                item['price_orig'] = orig
                item['price_sale'] = sale
                item['price_perc_discount'] = int(100-100*(sale/orig))
                item['price'] = item['price_sale']
                item['on_sale'] = 1 #BOOLEAN
            else:
                item['price_orig'] = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
                item['price_sale'] = ""
                item['on_sale'] = 0
        except IndexError:
            item['price_orig'] = int(float(response.selector.xpath('//div[@class="product_price"]/span[@id="ctl00_ContentMainPage_ctlSeparateProduct_lblProductPrice"]/text()').extract()[0][1:]))
            item['price'] = item['price_orig']
            item['price_sale'] = ""
            item['on_sale'] = 0 #BOOLEAN
        '''
        item['primary_color'] = ""
        tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
        item['tags'] = " ".join(tags)
        yield item
