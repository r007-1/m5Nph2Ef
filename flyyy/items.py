# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NuyolkItem(scrapy.Item):
    # define the fields for your item here like:
    ###objectID = scrapy.Field() WTFFF is this?!
    is_available = scrapy.Field()
    affiliate_partner = scrapy.Field()
    prod_id = scrapy.Field()
    merchant_prod_id = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant = scrapy.Field()

    merchant_country = scrapy.Field()
    merchant_language = scrapy.Field()
    currency_symbol = scrapy.Field()

    cat_code = scrapy.Field() #later
    mcat_code = scrapy.Field() #later
    brand = scrapy.Field()
    short_desc = scrapy.Field()
    long_desc = scrapy.Field() #new
    primary_color = scrapy.Field()
    currency = scrapy.Field()
    price_orig = scrapy.Field()
    price_sale = scrapy.Field()
    price_perc_discount = scrapy.Field() #whole number
    price = scrapy.Field()

    image_urls = scrapy.Field() #new
    images = scrapy.Field() #new

    img_1 = scrapy.Field()
    img_2 = scrapy.Field()
    img_3 = scrapy.Field()
    img_4 = scrapy.Field()
    img_5 = scrapy.Field()
    product_link = scrapy.Field()

    #new
    mcats = scrapy.Field()
    mcat_1 = scrapy.Field()
    mcat_2 = scrapy.Field()
    mcat_3 = scrapy.Field()
    mcat_4 = scrapy.Field()
    mcat_5 = scrapy.Field()

    imglinks = scrapy.Field()
    imglink_1 = scrapy.Field()
    imglink_2 = scrapy.Field()
    imglink_3 = scrapy.Field()
    imglink_4 = scrapy.Field()
    imglink_5 = scrapy.Field()
    imglink_5 = scrapy.Field()
    imglink_6 = scrapy.Field()

    cat_1 = scrapy.Field()
    cat_2 = scrapy.Field()
    cat_3 = scrapy.Field()

    tags = scrapy.Field()
    date_added = scrapy.Field()
    date_last_updated = scrapy.Field()
    on_sale = scrapy.Field()
    pass

class NeedSupplyAdditional(scrapy.Item):
    product_link = scrapy.Field()
    brand = scrapy.Field()
    mcats = scrapy.Field()
    mcat_code = scrapy.Field()
    mcat_1 = scrapy.Field()
    mcat_2 = scrapy.Field()
    mcat_3 = scrapy.Field()
    mcat_4 = scrapy.Field()
    mcat_5 = scrapy.Field()
    pass

class ShoptiquesAdditional(scrapy.Item):
    product_link = scrapy.Field()
    brand = scrapy.Field()
    mcats = scrapy.Field()
    mcat_code = scrapy.Field()
    mcat_1 = scrapy.Field()
    mcat_2 = scrapy.Field()
    mcat_3 = scrapy.Field()
    mcat_4 = scrapy.Field()
    mcat_5 = scrapy.Field()
    pass