from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
from flyyy.items import NuyolkItem
import time
import datetime
import random
import numpy as np
import numpy
import math
import csv

class Shoptiques(scrapy.Spider):
	name = "shoptiques"
	allowed_domains = ["shoptiques.com"]
	is_test_run = False
	is_run = True
	start_urls = []
	if (is_run):
		index = "http://www.shoptiques.com/sitemap/sitemap-index.xml"
		index = bs(requests.get(index).text, "lxml").find_all("sitemap")
		for sitemap in index:
			s = sitemap.findNext("loc").text
			if 'products' in s:
				tags = bs(requests.get(s).text, "lxml").find_all("url")
			for tag in tags:
				url = tag.findNext("loc").text
				start_urls.append(url)
		if is_test_run:
			#start_urls = start_urls[0:100]
			start_urls = start_urls[140927:140957]
	start_urls = list(np.unique(start_urls))
	def parse(self, response):
		datetime = int(str(int(time.time()*100))) #Don't change!
		random.seed(1412112 + datetime) #Don't change!
		item = NuyolkItem() #Don't change!
		item['brand'] = response.selector.xpath('//span[@itemprop="brand"]/a/text()').extract()[0]
		item['cat_code'] = ""
		item['cat_1'] = "" #deprecate
		item['cat_2'] = "" #deprecate
		item['cat_3'] = "" #deprecate
		item['currency'] = str(response.selector.xpath('//div[@class="currency"]/span[@class="code"]/text()').extract()[0])
		if item['currency'] == 'USD':
			item['currency_symbol'] = '$'
		else:
			item['currency_symbol'] = '?'

		item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
		item['date_last_updated'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
		#item['image_urls'] = response.selector.xpath('//ul[@id="image-carousel"]/li/a/@href').extract()
		item['image_urls'] = ""
		item['img_1'] = ""
		item['img_2'] = ""
		item['img_3'] = ""
		item['img_4'] = ""
		item['img_5'] = ""
		try:
			item['long_desc'] = response.selector.xpath('//div[@itemprop="description"]//text()').extract()[0]
		except:
			item['long_desc'] = ""
		mcats = response.selector.xpath('.//ul[@class="shoptiques-breadcrumb"]/li/a/text()').extract()

		for i in range(0, 5):
			attr = 'mcat_' + str(i + 1)
			try:
				item[attr] = mcats[i]
			except:
				item[attr] = ""

		item['mcat_code'] = "" #later #Do NLP predictions
		item['merchant_id'] = "3O056R"
		item['merchant_prod_id'] = ''
		try:
			orig = int(float(response.selector.xpath('//*[@id="product-detail"]//*[contains(@class, "retail")]/text()').extract()[0][1:]))
			sale = int(float(response.selector.xpath('//*[@id="product-detail"]//*[contains(@class, "sale")]/text()').extract()[0][1:]))
			if (orig != sale):
				item['price_orig'] = int(orig)
				item['price_sale'] = int(sale)
				item['price_perc_discount'] = int(100-100*(sale/orig))
				item['on_sale'] = True
				item['price'] = int(item['price_sale'])
			else:
				item['price_orig'] = orig
				item['price'] = orig
				item['on_sale'] = False
		except:
			try:
				item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/text()').extract()[0][1:]))
			except Exception as e:
				item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[1]/text()').extract()[0][1:]))
			item['price'] = item['price_orig']
			item['price_sale'] = item['price_orig']
			item['on_sale'] = False
			item['price_perc_discount'] = 0
		item['primary_color'] = "" #later
		item['prod_id'] = str(datetime) + str(int(random.uniform(100000, 999999))) #Don't change!
		item['product_link'] = str(response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0])
		item['short_desc'] = str(response.selector.xpath('//div[@id="product-detail"]/div[@class="product-name"]/h1/text()').extract()[0].strip()).strip().replace("  ","")

		t = [item['brand'], item['short_desc'], "Women", mcats, item['long_desc']]
		item['tags'] = " ".join(list(numpy.hstack(t)))

		item['imglinks'] = response.selector.xpath('//ul[@id="image-carousel"]/li/a/@href').extract()
		for i in range(0, 6):
			attr = 'imglink_' + str(i+1)
			if i < len(item['imglinks']):
				item[attr] = str(item['imglinks'][i])
			else:
				item[attr] = ""
		item['imglinks'] = ""
		item['is_available'] = True #Don't change! #Fix later!
		item['affiliate_partner'] = "viglink"
		item['merchant'] = "Shoptiques"
		yield item