from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import random
import time

#start 06/02/2016 03:18:22


class HBX(scrapy.Spider):
    name = "hbx"
    allowed_domains = ["hbx.com"]
    start_urls = []
    sitemaps = []

    for page in range(0, 50):
        sitemaps.append("http://hbx.com/sitemap-product.xml?page="+ str(page + 1))

    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            start_urls.append(tag.findNext("loc").text)
    start_urls[0:10]
    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime)

        item = NuyolkItem()
        item['is_available'] = True
        item['affiliate_partner'] = "viglink"

        item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999))))
        item['product_link'] = response.selector.xpath('/html/head/meta[23]/@content').extract()[0]

        item['merchant_prod_id'] = response.selector.xpath('//*[@id="product-summary"]/@data-id').extract()[0] #skipped
        item['merchant_id'] = "70856L"

        item['brand'] = response.selector.xpath('//h1[@class="brand"]/text()').extract()[0]
        item['short_desc'] = response.selector.xpath('//h1[@class="brand"]/text()').extract()[0]
        item['long_desc'] = response.selector.xpath('//*[@id="description"]/p[2]/text()').extract()[0]
        item['primary_color'] = "" #later

        item['currency'] = response.selector.xpath('//*[@id="currency"]/ul/li[1]/a/span/text()').extract()[0]

        #If item is on sale,
        if (response.selector.xpath("//span[@class='price-standard']/text()").extract() != []):
            item['price_orig'] = response.selector.xpath("//span[@class='regular-price]/@content").extract()[0][1:]
            item['price_sale'] = response.selector.xpath("//span[@class='sale-price]/@content").extract()[0][1:]
            item['price_perc_discount'] = int((1 - float(item['price_sale'])/float(item['price_orig']))*100)
            item['price'] = item['price_sale']
        else:
            item['price_orig'] = response.selector.xpath("//span[@class='price-sales']/text()").extract()[0][1:]
            item['price'] = item['price_orig']

        item['image_urls'] = response.selector.xpath('//*[@class="zoom masterTooltip"]/img/@src').extract() #new
        item['img_1'] = ""
        item['img_2'] = ""
        item['img_3'] = ""
        item['img_4'] = ""
        item['img_5'] = ""

        #new
        item['mcats'] = response.selector.xpath('//*[@id="main"]/div/div/ol/li/a/text()').extract()

        for i in range(0, len(item['mcats'])):
            attr = 'mcat_' + str(i+1)
            item[attr] = item['mcats'][i]

        item['cat_code'] = ""
        item['cat_1'] = "" #deprecate
        item['cat_2'] = "" #deprecate
        item['cat_3'] = "" #deprecate

        tags = [str(response.selector.xpath('//h1[@class="brand"]/a/text()').extract()[0]), str(response.selector.xpath('//h1[@class="product-name"]/text()').extract()[0]), str(" ".join(item['mcats'])), str(response.selector.xpath('/html/head/meta[4]/@content').extract()[0])]
        item['tags'] = " ".join(tags)

        item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

        yield item
