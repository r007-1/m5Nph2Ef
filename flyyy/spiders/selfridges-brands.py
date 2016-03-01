from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from flyyy.items import NuyolkItem
import random
import time

class Selfridges(scrapy.Spider):
	name = "selfridges-brands"
	allowed_domains = ["selfridges.com"]
	start_urls = []
	sitemaps = ["http://www.selfridges.com/sitemap_US_en_1.xml"]

	for sitemap in sitemaps:
		tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
		for tag in tags:
			start_urls.append(tag.findNext("loc").text)
	def parse(self, response):
		item = NuyolkItem() #Don't change!
		try:
			item['brand'] = str(response.selector.xpath('//*[@name="productDesc"]//p[@itemprop="brand"]/a/text()').extract()[0])
			mcats = response.selector.xpath('//nav[@id="breadcrumb"]//li/a/text()').extract()
            item['mcats'] = mcats[1:len(mcats)-1]
            item['merchant_prod_id'] = str(response.selector.xpath('//form[@name="productId"]/@value').extract()[0])
			item['product_link'] = str(response.selector.xpath('//*[@id="canonicalUrl"]/@href').extract()[0])
			for i in range(0, 5):
				attr = 'mcat_' + str(i+1)
				if i < len(item['mcats']):
					item[attr] = str(item['mcats'][i])
				else:
					item[attr] = ""
			yield item
		except Exception as e:
			return
