from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import random
import time
import csv
from algoliasearch import algoliasearch

class Shoptiques(scrapy.Spider):
	name = "shoptiques"
	allowed_domains = ["shoptiques.com"]
	start_urls = []
	sitemaps = ["http://www.shoptiques.com/sitemap/products"]
	for sitemap in sitemaps:
		tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
		for tag in tags:
			url = tag.findNext("loc").text
			start_urls.append(url)
	start_urls = start_urls[34119:45000]
	def parse(self, response):
		client = algoliasearch.Client("BTPCHYHQQY", "e68eda57aa7bd4b52dd27e9226dec21a")
		index = client.init_index('products')
		datetime = int(str(int(time.time()*100))) #Don't change!
		random.seed(1412112 + datetime) #Don't change!
		item = NuyolkItem() #Don't change!
		item['brand'] = "" #Needs post-processing!
		item['cat_code'] = ""
		item['cat_1'] = "" #deprecate
		item['cat_2'] = "" #deprecate
		item['cat_3'] = "" #deprecate
		item['currency'] = str(response.selector.xpath('//div[@class="currency"]/span[@class="code"]/text()').extract()[0])
		item['date_added'] = str(time.strftime("%d/%m/%Y %H:%M:%S"))
		#item['image_urls'] = response.selector.xpath('//ul[@id="image-carousel"]/li/a/@href').extract()
		item['img_1'] = ""
		item['img_2'] = ""
		item['img_3'] = ""
		item['img_4'] = ""
		item['img_5'] = ""
		try:
			item['long_desc'] = str(response.selector.xpath('//div[@itemprop="description"]/p/text()').extract()[0].strip())
		except Exception as e:
			item['long_desc'] = ""
		item['mcats'] = "" #later #Do NLP predictions
		item['mcat_1'] = "" #later #Do NLP predictions
		item['mcat_2'] = "" #later #Do NLP predictions
		item['mcat_3'] = "" #later #Do NLP predictions
		item['mcat_4'] = "" #later #Do NLP predictions
		item['mcat_5'] = "" #later #Do NLP predictions
		item['mcat_code'] = "" #later #Do NLP predictions
		item['merchant_id'] = "3O056R"
		item['merchant_prod_id'] = ''
		try:
			orig = int(float(response.selector.xpath('//*[@id="product-detail"]//*[contains(@class, "retail")]/text()').extract()[0][1:]))
			sale = int(float(response.selector.xpath('//*[@id="product-detail"]//*[contains(@class, "sale")]/text()').extract()[0][1:]))
			if (orig != sale):
				item['price_orig'] = orig
				item['price_sale'] = sale
				item['price_perc_discount'] = int(100-100*(sale/orig))
				item['price'] = item['price_sale']
			else:
				item['price_orig'] = orig
				item['price'] = orig
		except IndexError:
			try:
				item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/text()').extract()[0][1:]))
			except Exception as e:
				item['price_orig'] = int(float(response.selector.xpath('//div[@class="product-name"]/span[@id="product-price"]/span/span[1]/text()').extract()[0][1:]))
			item['price'] = item['price_orig']
		item['primary_color'] = "" #later
		item['prod_id'] = int(str(datetime) + str(int(random.uniform(100000, 999999)))) #Don't change!
		item['product_link'] = str(response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0])
		item['short_desc'] = str(response.selector.xpath('//div[@id="product-detail"]/div[@class="product-name"]/h1/text()').extract()[0].strip()).strip().replace("  ","")
		tags = [str(item['brand']), str(item['short_desc']), str(item['long_desc'])] #str(" ".join(item['mcats'])),
		item['tags'] = " ".join(tags)
		item['imglinks'] = response.selector.xpath('//ul[@id="image-carousel"]/li/a/@href').extract()
		for i in range(0, 6):
			attr = 'imglink_' + str(i+1)
			if i < len(item['imglinks']):
				item[attr] = str(item['imglinks'][i])
			else:
				item[attr] = ""
		item['is_available'] = True #Don't change! #Fix later!
		item['affiliate_partner'] = "viglink"
		item['objectID'] = item['prod_id']
		item['merchant'] = "Shoptiques"
		product = {}
		for attr in item.keys():
			product[attr] = item[attr]
		res = index.save_object(product)
		yield item
