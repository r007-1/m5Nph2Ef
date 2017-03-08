import json
import pandas
from presignups_app.models import Product
import math
import datetime
from django.utils import timezone
import os
import random
import re
import codecs

def add():
    #items = pandas.read_json('admin_products/spiders/json/barneys.json')
    os.chdir('/Users/MacbookPro/Documents/nuylkr')
    items = pandas.read_json('030316-145k.json')
    i = items
    items = i[0:10]
    for item in range(0, len(items)):
        newItem = Product.objects.create(id=items['prod_id'][item], prod_id=items['prod_id'][item], cat_code=items['cat_code'][item], mcat_5=items['mcat_5'][item], mcat_1=items['mcat_1'][item], mcat_2=items['mcat_2'][item], mcat_3=items['mcat_3'][item], on_sale=items['on_sale'][item], currency=items['currency'][item], price_perc_discount=items['price_perc_discount'][item], cat_1=items['cat_1'][item], cat_2=items['cat_2'][item], cat_3=items['cat_3'][item], short_desc=items['short_desc'][item], imglink_4=items['imglink_4'][item], primary_color=items['primary_color'][item], mcat_code=items['mcat_code'][item], brand=items['brand'][item], merchant=items['merchant'][item], date_last_updated=items['date_last_updated'][item], long_desc=items['long_desc'][item], tags=items['tags'][item], price=items['price'][item], price_orig=items['price_orig'][item], image_urls=items['image_urls'][item], is_available=items['is_available'][item], date_added=items['date_added'][item], merchant_id=items['merchant_id'][item], affiliate_partner=items['affiliate_partner'][item], img_5=items['img_5'][item], img_4=items['img_4'][item], img_1=items['img_1'][item], img_3=items['img_3'][item], img_2=items['img_2'][item], imglink_5=items['imglink_5'][item], merchant_prod_id=items['merchant_prod_id'][item], imglink_6=items['imglink_6'][item], product_link=items['product_link'][item], imglink_3=items['imglink_3'][item], imglink_2=items['imglink_2'][item], imglink_1=items['imglink_1'][item], mcat_4=items['mcat_4'][item], currency_symbol=items['currency_symbol'][item], price_sale=items['price_sale'][item])
        newItem.save()
        print(str(item) + "saved")
    print("Done!")

"""
        mc = {}
        for i in range(0, 6):
            if i < len(items['mcats'][item]):
                mc['mc_' + str(i + 1)] = items['mcat_' + str(i + 1)][item]
            else:
                mc['mc_' + str(i + 1)] = ""
        imgs = []
        imgnum = {}
        temp = items['images'][item]
        if temp is not []:
            temp = pandas.DataFrame(items['images'][item])
        for i in range(0, 5):
            if i < len(temp):
                imgs.append(str(temp['path'][i])[6:])
                imgnum["img_" + str(i+1)] = 'products/photos/' + str(temp['path'][i])[6:]
            else:
                imgnum["img_" + str(i+1)] = ""
        if not isinstance(items.loc[item, 'price_sale'], unicode):
            items.loc[item, 'price_sale'] = 0
        else:
            try:
                items.loc[item, 'price_sale'] = int(str(items.loc[item, 'price_sale']).replace(',', ''))
            except ValueError:
                items.loc[item, 'price_sale'] = 0
        if not isinstance(items.loc[item, 'price_orig'], unicode):
            items.loc[item, 'price_orig'] = 0
        else:
            try:
                items.loc[item, 'price_orig'] = int(str(items.loc[item, 'price_orig']).replace(',', ''))
            except ValueError:
                items.loc[item, 'price_orig'] = 0
        if not isinstance(items.loc[item, 'price_perc_discount'], unicode):
            items.loc[item, 'price_perc_discount'] = 0
        else:
            try:
                items.loc[item, 'price_perc_discount'] = int(str(items.loc[item, 'price_perc_discount']).replace(',', ''))
            except ValueError:
                items.loc[item, 'price_perc_discount'] = 0
        if not isinstance(items.loc[item, 'price'], unicode):
            items.loc[item, 'price'] = 0
        else:
            try:
                items.loc[item, 'price'] = int(str(items.loc[item, 'price']).replace(',', ''))
            except ValueError:
                items.loc[item, 'price'] = 0
        date_added = timezone.now()
        date_last_updated = timezone.now()
        newItem = Product(date_added=date_added, date_last_updated=date_last_updated, prod_id=str(items['prod_id'][item]), merchant_id=str(items['merchant_id'][item]), merchant_prod_id=str(items['merchant_prod_id'][item]), is_available=True, brand=str(items['brand'][item]), short_desc=str(items['short_desc'][item]), long_desc=str(items['long_desc'][item]), currency=str(items['currency'][item]), price_orig=int(items['price_orig'][item]), price_sale=int(items['price_sale'][item]), price_perc_discount=int(items['price_perc_discount'][item]), price=int(items['price'][item]), product_link=str(items['product_link'][item]), tags=str(items['tags'][item]), affiliate_partner="viglink", img_1=imgnum['img_1'], img_2=imgnum['img_2'], img_3=imgnum['img_3'], img_4=imgnum['img_4'], img_5=imgnum['img_5'], primary_color=str(items['primary_color'][item]), mcat_1=str(mc['mc_1']), mcat_2=str(mc['mc_2']), mcat_3=str(mc['mc_3']), mcat_4=str(mc['mc_4']), mcat_5=str(mc['mc_5']), mcat_6=str(mc['mc_6']), cat_1=str(items['cat_1'][item]), cat_2=str(items['cat_2'][item]), cat_3=str(items['cat_3'][item]))
        """
def hex(pid):
    pid = str(pid)
    oid = random.choice('abcdef') + pid[0:1] + random.choice('abcdef') + pid[1:5] + random.choice('abcdef') + pid[5:8]
    oid = oid + random.choice('abcdef') + pid[8:17] + random.choice('abcdef') + pid[17:] + random.choice('abcdef')
    return oid

def clean(text):
    ascii = ''.join(i for i in text if ord(i) < 128)
    ascii = re.sub(r'[^\x00-\x7F]', '', ascii)
    text = ascii.decode('ascii').encode('utf-8')
    return text

def mongoformat(file):
    os.chdir('/Users/MacbookPro/Documents/nuylkr')
c = codecs.open(file, 'r', 'utf-8')
items = pandas.read_json(c)
items_ = items
items = items_[0:10]
products = list()
for item in range(0, len(items)):
    current = items.loc[item]
    keys = list(current.keys())
    values = list(current)
    product = dict()
    product['_id'] = {'$oid': str(hex(values[keys.index('prod_id')]))}
    products.append(product)
    print(item)


p = products
p = str(p).replace('{\'', '{\"')
p = str(p).replace('\': \'', '\": \"')
p = str(p).replace('\', \'', '\", \"')
p = str(p).replace('\'}', '\"}')
p = str(p).replace('\': ', '\": ')
p = str(p).replace('\': ', '\": ')
p = str(p).replace(', \'', ', \"')
p = str(p).replace('$', '\x24')

p = str(p).replace('long_desc\": in ', 'long_desc\": \"')
p = str(p).replace('long_desc\": \"\"', 'long_desc\": \"')
p = str(p).replace('0.5 \"', '0.5 in')
p = str(p).replace(' \" ', ' in ')
p = str(p).replace(' \"X\" ', ' X ')
p = str(p).replace('Tribe\\\'s" ', 'Tribe\'s ')
p = str(p).replace('\"\"The Stussy" ', '\"The Stussy')
p = str(p).replace('   \"The Stussy ', '   The Stussy ')

save = open('sample46.json', 'w')
save.write(p)
save.close()

s = products[0:10]

with open('s0.json', 'w') as outfile:
    outfile.write(json.dumps(s, outfile, indent=4))

isthisit = products

with open('finally.json', 'w') as outfile:
    outfile.write(json.dumps(isthisit, outfile, indent=4))

grrr = []
for i in range(0, 10):
    p = str(products[i])
    grrr.append(len(p) - len(p.replace('\'','')))

def edited(index):
    return p[len(str(products[0:index-1])):len(str(products[0:index-1]))+(len(str(products[index])))]

def delete_by_query(file):
    f = open(file, 'r')
    items = json.load(f)
    for item in items:
        if item['price'] == 0: #change to needed condition
            items.remove(item)
    with open('finally-finally.json', 'w') as outfile:
        outfile.write(json.dumps(items, outfile, indent=4))

def mongoformat(file):
    os.chdir('/Users/MacbookPro/Documents/nuylkr')
c = codecs.open(file, 'r', 'utf-8')
items = pandas.read_json(c)
items_ = items
items = items_[0:10]
products = list()
for item in range(0, len(items)):
    current = items.loc[item]
    keys = list(current.keys())
    values = list(current)
    product = dict()
    product['_id'] = {'$oid': str(hex(values[keys.index('prod_id')]))}
    for k in range(0, len(keys)):
        if isinstance(values[k], unicode) or isinstance(values[k], str):
            product[str(keys[k])] = str(clean(values[k]))
        else:
            product[str(keys[k])] = values[k]
    products.append(product)
    print(item)


p = products
p = str(p).replace('{\'', '{\"')
p = str(p).replace('\': \'', '\": \"')
p = str(p).replace('\', \'', '\", \"')
p = str(p).replace('\'}', '\"}')
p = str(p).replace('\': ', '\": ')
p = str(p).replace('\': ', '\": ')
p = str(p).replace(', \'', ', \"')
p = str(p).replace('$', '\x24')

p = str(p).replace('long_desc\": in ', 'long_desc\": \"')
p = str(p).replace('long_desc\": \"\"', 'long_desc\": \"')
p = str(p).replace('0.5 \"', '0.5 in')
p = str(p).replace(' \" ', ' in ')
p = str(p).replace(' \"X\" ', ' X ')
p = str(p).replace('Tribe\\\'s" ', 'Tribe\'s ')
p = str(p).replace('\"\"The Stussy" ', '\"The Stussy')
p = str(p).replace('   \"The Stussy ', '   The Stussy ')

save = open('sample46.json', 'w')
save.write(p)
save.close()

s = products[0:10]

with open('s0.json', 'w') as outfile:
    outfile.write(json.dumps(s, outfile, indent=4))

isthisit = products

with open('finally.json', 'w') as outfile:
    outfile.write(json.dumps(isthisit, outfile, indent=4))

grrr = []
for i in range(0, 10):
    p = str(products[i])
    grrr.append(len(p) - len(p.replace('\'','')))
