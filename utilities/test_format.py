from bs4 import BeautifulSoup as bs
from lxml import etree, html
import requests
import scrapy
import pandas
import time
import datetime
import random
import numpy as np
import math
from collections import Counter
import csv
import numpy
import json
import os

fn = "test/0918_asos_test4.json"

def test_output(test_name, test, t):
    if (test):
        print("[/] " + test_name)
    else:
        print("[X] " + test_name)
    t[test_name] = test
    return

def is_attr_type(attr_name, type, ff):
    test_array = [isinstance(x[attr_name], type) for x in ff]
    test = sum(test_array) == len(test_array)
    return test

def remove_duplicates(fn):
    f = open(fn, 'r')
    ff = json.load(f)
    f.close()
    products = pandas.DataFrame(ff)

    links = [x["product_link"] for x in ff]
    are_links_uniq = len(links) == len(np.unique(links))
    if (not are_links_uniq):
        c = Counter(links)
        ck = c.keys()
        cv = c.values()
        di = numpy.where(numpy.array(cv) > 1)[0]
        oi = numpy.where(numpy.array(cv) == 1)[0]

        duplicate_links = numpy.array(ck)[di]
        is_duplicate = [x in duplicate_links for x in products.loc[:,"product_link"]]
        duplicate_indices = numpy.array(range(len(products)))[numpy.array(is_duplicate)]
        duplicates = dict(zip(duplicate_indices, products.loc[duplicate_indices, "product_link"]))
        duplicate_products = products.loc[duplicate_indices,:]

        is_not_duplicate = [not x for x in is_duplicate]
        ok_indices = numpy.array(range(len(products)))[numpy.array(is_not_duplicate)]
        ok_products = products.loc[ok_indices, :]

        fixed_indices = []
        for d in numpy.unique(duplicate_links):
            f = [key for key, value in duplicates.iteritems() if value == d][0]
            fixed_indices.append(f)

        rm = list(set(duplicate_indices) - set(fixed_indices))
        keep = list(set(range(len(ff)))-set(rm))
        z = list(numpy.array(ff)[numpy.array(keep)])

        os.remove(fn)
        fn = fn.replace(".json", "") + "_nd" + ".json"
        with open(fn, 'w') as outfile:
            json.dump(z, outfile)

def test_format_postmine(fn):
    f = open(fn, 'r')
    ff = json.load(f)
    f.close()

    t = {}

    ## Unique product links
    product_links = [x["product_link"] for x in ff]
    are_links_uniq = len(product_links) == len(np.unique(product_links))
    test_output("The product links are unique", are_links_uniq, t)

    ## prod_id type is str
    is_prod_id_str = is_attr_type("prod_id", str, ff) or is_attr_type("prod_id", unicode, ff)
    test_output("The prod_id type is str", is_prod_id_str, t)

    ## on_sale and is_available are boolean
    test_output("The on_sale type is bool", is_attr_type("on_sale", bool, ff), t)
    test_output("The is_available type is bool", is_attr_type("is_available", bool, ff), t)

    ## Make sure there are no list items
    has_no_list = True
    for k in ff[0].keys():
        has_no_list = has_no_list or is_attr_type(k, list, ff)
    test_output("There are no list types", has_no_list, t)

    ## Prices should be ints
    price_attrs = ['price', 'price_orig', 'price_perc_discount', 'price_sale']
    for p in price_attrs:
        test_output("The " + p + " type is int", is_attr_type(p, int, ff), t)

    ## Dates should be strings
    date_attrs = ["date_added", "date_last_updated"]
    for d in date_attrs:
        test_output("The " + d + " type is str", is_attr_type(d, str, ff) or is_attr_type(d, unicode, ff), t)

    ## TODO Make sure there are no useless crap in long_desc

    ## Has correct list of 43 attrs
    corr_attrs = [u'affiliate_partner', u'brand', u'cat_1', u'cat_2', u'cat_3', u'cat_code', u'currency', u'currency_symbol',
     u'date_added', u'date_last_updated', u'image_urls', u'img_1', u'img_2', u'img_3', u'img_4', u'img_5', u'imglink_1',
     u'imglink_2', u'imglink_3', u'imglink_4', u'imglink_5', u'imglink_6', u'is_available', u'long_desc', u'mcat_1',
     u'mcat_2', u'mcat_3', u'mcat_4', u'mcat_5', u'mcat_code', u'merchant', u'merchant_id', u'merchant_prod_id',
     u'on_sale', u'price', u'price_orig', u'price_perc_discount', u'price_sale', u'primary_color', u'prod_id',
     u'product_link', u'short_desc', u'tags']
    data_attrs = sum([x in corr_attrs for x in ff[0].keys()]) == 43

    ## Currency has to be USD
    currencies = [x['currency']=='USD' for x in ff]
    are_usd = sum(currencies) == len(currencies)
    test_output("Currency is in USD", are_usd, t)

    ## Summary
    is_okay = sum(t.values()) == len(t.values())
    if (is_okay):
        print("YAY!!!")
    else:
        print("UGHHH!!! Fix the following:")
        errors = np.array(t.keys())[np.array([not x for x in t.values()])]
        for i in range(len(errors)):
            print(str(i+1) + ": " + errors[i])
    return is_okay

def convert_to_usd(fn):
    f = open(fn, 'r')
    ff = json.load(f)
    f.close()
    products = pandas.DataFrame(ff)

    current = str(ff[0]['currency'])
    target = 'USD'

    api = "http://api.fixer.io/latest?symbols=USD,PHP"
    response = json.loads(requests.get(api).content)
    rate = response['rates'][target]/response['rates'][current]

    price_attrs = ['price', 'price_orig', 'price_perc_discount', 'price_sale']

    for attr in price_attrs:
        products.loc[:, attr] = [int(x*rate) for x in products.loc[:, attr]]

    products.loc[:, "currency"] = target
    products.loc[:, "currency_symbol"] = '$'

    if (False):
        products.loc[:, "tags"] = [" ".join(x) for x in products.loc[:, "tags"]]

    z = json.loads(products.to_json(orient='records'))
    fn = fn.replace(".json", "") + "_usd" + ".json"
    with open(fn, 'w') as outfile:
        json.dump(z, outfile)
    return z
