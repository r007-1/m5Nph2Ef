from bs4 import BeautifulSoup as bs
import requests
import scrapy
from lxml import etree
from flyyy.items import ShoptiquesAdditional
import random
import time
import scrapy

class ShoptiquesBrands(scrapy.Spider):
  name = "shoptiques-brands"
  allowed_domains = ["shoptiques.com"]
  start_urls = []
  sitemaps = ["http://www.shoptiques.com/sitemap/products"]

  for sitemap in sitemaps:
    tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
  for tag in tags:
    if (tag.findNext("loc").text[len(tag.findNext("loc").text)-1] == "."):
      start_urls.append(tag.findNext("loc").text[0:len(tag.findNext("loc").text)-1])
    else:
      start_urls.append(tag.findNext("loc").text)
  def parse(self, response):
      try:
        item = ShoptiquesAdditional() #Don't change!
        item['product_link'] = str(response.selector.xpath('//link[@rel="canonical"]/@href').extract()[0])
        item['brand'] = str(response.selector.xpath('//*[@class="accordion-inner"]//a[contains(@href,"brands")]/text()').extract()[0])
        item['mcats'] = response.selector.xpath('//*[@class="shoptiques-breadcrumb"]/li/a[contains(@href,"categories")]/text()').extract()
        for i in range(0, 5):
          attr = 'mcat_' + str(i+1)
          if i < len(item['mcats']):
            item[attr] = str(item['mcats'][i])
            if i == len(item['mcats']) - 1:
              item['mcat_code'] = item[attr]
        yield item
      except Exception as e:
          pass
    #str(response.selector.xpath('//*[@class="details"]/h2//text()').extract()[0])
    #/html/head/meta[8]