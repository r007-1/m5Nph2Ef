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


#### CRAWLER BLOCKED


class Selfridges(scrapy.Spider):
	name = "selfridges"
	allowed_domains = ["selfridges.com"]

	is_run = False
	is_test = True

	start_urls = []
	sitemap_main = "http://www.selfridges.com/sitemap.xml"
	sitemaps = []
	if (is_run):
		tags = bs(requests.get(sitemap_main).text, "lxml").find_all("sitemap")
		for tag in tags:
			t = tag.findNext("loc").text
			if "US_en" in t:
				sitemaps.append(t)
		for sitemap in sitemaps:
			tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
			for tag in tags:
				url = tag.findNext("loc").text
				if '/cat/' in url and url.count('-') >= 2:
					start_urls.append(url)
		if (is_test):
			start_urls = start_urls[1000:1100]
	start_urls = list(np.unique(start_urls))
	def parse(self, response):
		datetime = int(str(int(time.time()*100))) #Don't change!
		random.seed(1412112 + datetime) #Don't change!
		item = NuyolkItem() #Don't change!
		try:
			item['brand'] = response.selector.xpath('//span[@class="brand"]/a/text()').extract()[0]
			item['cat_code'] = ""
			item['cat_1'] = "" #deprecate
			item['cat_2'] = "" #deprecate
			item['cat_3'] = "" #deprecate
			item['currency'] = str(response.selector.xpath('//*[@class="translateFlag"]/a/span/text()').extract()[0])
			response.selector.path('//*[@id="currencyLink"]/span')
			item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
			images=[]
			images.append(response.selector.xpath('//div[@class="productImage"]//img/@data-rvsrc').extract()[0])
			if images[0] == []:
				images = []
				images.append(response.selector.xpath('//*[@class="pImgWrap"]/img/@src').extract())
			#item['image_urls'] = images
			item['img_1'] = ""
			item['img_2'] = ""
			item['img_3'] = ""
			item['img_4'] = ""
			item['img_5'] = ""
			long_desc = response.selector.xpath('//div[@class="selfridgesSaysInner"]/div/p[@class="hiddenDescription"]/text()').extract()[0].strip() ##encoding problem
			item['long_desc'] = long_desc.replace("<b>", "").replace("</b>", "")
			item['mcats'] = "" #later #Do NLP predictions
			item['mcat_1'] = "" #later #Do NLP predictions
			item['mcat_2'] = "" #later #Do NLP predictions
			item['mcat_3'] = "" #later #Do NLP predictions
			item['mcat_4'] = "" #later #Do NLP predictions
			item['mcat_5'] = "" #later #Do NLP predictions
			item['merchant_id'] = "TO663Y"
			item['merchant_prod_id'] = str(response.selector.xpath('//p[@class="pcode"]/span[@class="val"]/text()').extract()[0].strip())
			try:
				orig = int(float(str(response.selector.xpath('//p[@class="wasPrice"]/text()').extract()[0]).strip().replace(",","")[1:]))
				sale = int(float(str(response.selector.xpath('//p[@class="price red"]/span[2]/text()').extract()[0]).strip().replace(",","")))
				if (orig != sale):
					item['price_orig'] = orig
					item['price_sale'] = sale
					item['price_perc_discount'] = int(100-100*sale/orig)
					item['price'] = sale
				else:
					item['price_orig'] = orig
					item['price'] = orig
			except IndexError:
				item['price_orig'] = int(float(str(response.selector.xpath('//p[@class="price"]/span[2]/text()').extract()[0]).strip().replace(",","")))
				item['price'] = item['price_orig']
			item['primary_color'] = "" #later
			item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999)))) #Don't change!
			item['product_link'] = response.selector.xpath('//link[@rel="canonical"]/@href').extract()[0]
			item['short_desc'] = str(response.selector.xpath('//head/title/text()').extract()[0])
			tags = [str(item['brand']), item['short_desc'], item['long_desc']] #str(" ".join(item['mcats'])),
			item['tags'] = " ".join(tags)
			item['date_last_updated'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
			item['merchant'] = 'Selfridges'
			item['imglinks'] = images
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
