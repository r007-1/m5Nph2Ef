from bs4 import BeautifulSoup as bs
import requests
import scrapy
from lxml import etree
from flyyy.items import ShoptiquesAdditional
import scrapy

class Shoptiques(scrapy.Spider):
	name = "shoptiques-brands"
	allowed_domains = ["shoptiques.com"]
	start_urls = []
	sitemaps = ["http://www.shoptiques.com/sitemap/products"]
	for sitemap in sitemaps:
		tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
		for tag in tags:
			url = tag.findNext("loc").text
			start_urls.append(url)
  def parse(self, response):
    item = ShoptiquesAdditional() #Don't change!
    try:
      item['product_link'] = str(response.selector.xpath('//link[@rel="canonical"]/@href').extract()[0])
      item['brand'] = str(response.selector.xpath('//*[@class="accordion-inner"]//a[contains(@href,"brands")]/text()').extract()[0])
      item['mcats'] = response.selector.xpath('//*[@class="shoptiques-breadcrumb"]/li/a[contains(@href,"categories")]/text()').extract()
      for i in range(0, 5):
        attr = 'mcat_' + str(i+1)
        if i < len(item['mcats']):
          item[attr] = str(item['mcats'][i])
          if i == len(item['mcats']) - 1:
            item['mcat_code'] = item[attr]
        else:
          item[attr] = ""
      yield item
    except Exception as e:
      return