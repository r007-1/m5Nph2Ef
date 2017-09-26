from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import math
##import numpy
import csv

### CRAWLER BLOCKEd

class NeedSupply(scrapy.Spider):
    name = "needsupply"
    allowed_domains = ["needsupply.com"]
    start_urls = []
    majcat = ["http://needsupply.com/mens/", "http://needsupply.com/womens/"]
    cat_urls = []

    for mc in majcat:
        m = html.fromstring(requests.get(mc).content)
        m.xpath('.//li[@class="category"]')
        m.xpath('.//li[contains(@class, "category-link")]/@href')

    sitemap = "https://needsupply.com/media/sitemap.xml"

    tags = bs(requests.get(sitemap).text, "lxml").find_all("loc")
    for tag in tags:
        if (tag.findNext("loc").text[len(tag.findNext("loc").text)-1] == "."):
          start_urls.append(tag.findNext("loc").text[0:len(tag.findNext("loc").text)-1])
        else:
          start_urls.append(tag.findNext("loc").text)
    s = start_urls
    start_urls = s[28000:28010]

    def parse(self, response):
        datetime = int(str(int(time.time()*100)))
        random.seed(1412112 + datetime) #Don't change!
        item = NuyolkItem() #Don't change!
        try:
          test = str(response.selector.xpath('//div[@id="product-old"]/form/input[@name="product"]/@value').extract()[0])

          item['brand'] = "" #Needs post-processing!

          item['cat_code'] = ""
          item['cat_1'] = "" #deprecate
          item['cat_2'] = "" #deprecate
          item['cat_3'] = "" #deprecate

          curr = '//*[@id="currency-widget"]/li['+str(len(response.selector.xpath('//*[@id="currency-widget"]/li').extract()))+']/a/span'
          curr_temp = response.selector.xpath(curr).extract()[0]
          item['currency'] = str(curr_temp[curr_temp.index(">")+1:curr_temp.rindex("<")])
          item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))

          #item['image_urls'] = response.selector.xpath('//ul[@class="thumbs"]/li/a/img/@src').extract()
          item['img_1'] = ""
          item['img_2'] = ""
          item['img_3'] = ""
          item['img_4'] = ""
          item['img_5'] = ""

          long_desc = response.selector.xpath('//p[@class="description"]/text()').extract()
          #item['long_desc'] = " ".join(long_desc).replace('\n', '').replace('\t', '').replace('\r', '').replace(u"\u2022", "")
          item['long_desc'] = " ".join(long_desc)

          item['mcats'] = "" #later #Do NLP predictions
          item['mcat_1'] = ""
          item['mcat_1'] = ""
          item['mcat_1'] = ""
          item['mcat_1'] = ""
          item['mcat_1'] = ""
          item['mcat_1'] = ""
          item['mcat_code'] = ""

          item['merchant_id'] = "JOQ3F3"
          item['merchant_prod_id'] = str(response.selector.xpath('//div[@id="product-old"]/form/input[@name="product"]/@value').extract()[0])

          try:
            if (response.selector.xpath("//div[@class='price-mobile']/p/span[@class='price']/text()").extract()[0] != response.selector.xpath("//div[@class='price-mobile']/h3/span[@class='price']/text()").extract()[0]):
              item['price_orig'] = int(float(response.selector.xpath("//div[@class='price-mobile']/p/span[@class='price']/text()").extract()[0][1:]))
              item['price_sale'] = int(float(response.selector.xpath("//div[@class='price-mobile']/h3/span[@class='price']/text()").extract()[0][1:]))
              item['price_perc_discount'] = int(100-((float(response.selector.xpath("//div[@class='price-mobile']/h3/span[@class='price']/text()").extract()[0][1:]))/(float(response.selector.xpath("//div[@class='price-mobile']/p/span[@class='price']/text()").extract()[0][1:])))*100)
              item['price'] = item['price_sale']
            else:
              item['price_orig'] = int(float(response.selector.xpath("//div[@class='price-mobile']/h3/span[@class='price']/text()").extract()[0][1:]))
              item['price'] = item['price_orig']
          except IndexError:
            item['price_orig'] = int(float(response.selector.xpath("//div[@class='price-mobile']/h3/span[@class='price']/text()").extract()[0][1:]))
            item['price'] = item['price_orig']

          item['primary_color'] = "" #later
          item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999)))) #Don't change!
          item['product_link'] = str(response.selector.xpath('//link[@rel="canonical"]/@href').extract()[0])

          item['short_desc'] = str(response.selector.xpath('//title/text()').extract()[0])
          tags = [str(item['brand']), str(item['short_desc']), item['long_desc']] #str(" ".join(item['mcats'])),
          item['tags'] = " ".join(tags)

          item['imglinks'] = response.selector.xpath('//ul[@class="thumbs"]/li/a/img/@src').extract()
          for i in range(0, 6):
            attr = 'imglink_' + str(i+1)
            if i < len(item['imglinks']):
              item[attr] = str(item['imglinks'][i])
            else:
              item[attr] = ""

          item['is_available'] = True #Don't change! #Fix later!
          item['affiliate_partner'] = "viglink"
          yield item
        except Exception as e:
          return
