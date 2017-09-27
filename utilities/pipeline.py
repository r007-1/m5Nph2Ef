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
from utilities.test_format import test_output, is_attr_type, remove_duplicates, test_format_postmine, convert_to_usd
from post_processing.category import generate_cat
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pymongo import MongoClient
import pymongo


###### TODO: Figure out file format for each step
###### TODO: Create logs in Sheets


## Check if script is up-to-date


## Mine continuously
#### TODO: Fool-proof in case of connection failure




fn = "products/hbx_20170918_usd.json"

## Double check format
#### Fix format deficiencies until okay
is_okay = test_format_postmine(fn)
if (not is_okay):
    print('ERRORRRR')


## Add category
if (is_okay):
    rfunc = '/Users/lovetteregner/Documents/pipeline_old/m5Nph2Ef/post_processing/categorization_clean_data.R'
    expr = "".join(["R CMD BATCH --no-save --no-restore \'--args fn=\"", fn, "\"", "\' ", rfunc, " R.out"])
    pre = int(datetime.datetime.now().strftime("%s"))
    os.system(expr)
    mtime = os.path.getmtime('R.out')
    is_recent = mtime - pre > 0
    if (is_recent):
        f = open('R.out', 'r')
        rout = f.read()
        is_successful = rout.find("Success!") > 0
        if (is_successful):
            fn = fn.replace(".json", "_cleanshld.json")
            d = generate_cat(fn)
            fn = fn.replace(".json", "_with_cat.json")
            is_okay = test_format_postmine(fn)
            if (is_okay):
                print("YAY! YAY! YAY!")
            else:
                print("Check the format of the output of generate_cat()")
        else:
            print("There was an error while executing the clean_ld() cmd.")
    else:
        print("The clean_ld() cmd was not called.")



###
# fn = "products/ahalife_20170919.json"
if 'd' not in globals():
    fn = fn.replace(".json", "_cleanshld.json")
    fn = fn.replace(".json", "_with_cat.json")
    f = open(fn, 'r')
    data = json.load(f)
    d = data
    f.close()

## Update MongoDB
#### If prod_id exists, update variables
#### Else, upload
data = d
time_now = str(time.strftime("%d/%m/%Y %H:%M:%S"))
for i in range(len(data)):
    data[i]['date_last_updated'] = time_now


## Run only once: change _ids to prod_ids
is_first_run = True
if (is_first_run):
    delete_existing = True
    es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')
    q = 'merchant: ' + str(data[0]['merchant'])
    qq = {
        'from': 0,
        'size': 10000,
        'query': {
            'query_string': {'query': q}
        }
        ,"_source": ["date_last_updated", "product_link", "prod_id"]
    }
    h = list()
    r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
    total = r['hits']['total']
    batches = int(math.ceil(total*1.0/qq['size']))
    for i in range(0, batches):
        if i==0:
            r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            h.extend(hits)
        else:
            r = es.scroll(scroll_id=sid, scroll='1m')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            h.extend(hits)
    hits = h
    validhits = [x['_source']!={} for x in hits]
    hits = numpy.array(hits)[numpy.array(validhits)]

    if (delete_existing):
        ## Delete product_link if exists in prod_id != '_id (one-off adjustment)
        new_links = [x['product_link'] for x in data]
        linksss = [x['_source']['product_link'] for x in hits]
        will_del = [x['_source']['product_link'] in new_links and x['_id'] != x['_source']['prod_id'] for x in hits]
        ids = [x['_id'] for x in hits]
        del_ids = numpy.array(ids)[numpy.array(will_del)]
        delete = [{"_id": d, "_type": "product", "_index": "products", '_op_type': 'delete'} for d in del_ids]
        batches = int(math.ceil(len(delete)/100.0))
        for i in range(0, batches):
            dels = delete[i*100:min((i+1)*100, len(delete))]
            helpers.bulk(es, dels, chunk_size=100)
            print(min((i+1)*100, len(delete)))

if (is_okay):
    client = MongoClient('mongodb://engineering:ZrcyknglNEC1E78KQhI6Q3Y8iWyd4nW7@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
    db = client.glarket
    products = db.products
    batches = int(math.ceil(len(data) / 50.0))
    for i in range(0, batches):
        upload = data[i * 50:min((i + 1) * 50, len(data))]
        reqs = [pymongo.ReplaceOne({'product_link': x['product_link']}, x, upsert=True) for x in upload]
        try:
            result = products.bulk_write(reqs, ordered=False)
            print(result.bulk_api_result)
            print("Batch: " + str(i) + "/" + str(batches) + "; "+ str(i/(batches*1.0)*100) + "%")
        except BulkWriteError as bwe:
            print(bwe.details)

## Update ES
#### If prod_id exists, update variables
#### Else, upload
es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')

##Permanent
#up = [{"_id": prod['prod_id'], "doc_as_upsert": True,  "_type": "product", "_index": "products", "_source": {'doc': prod}, '_op_type': 'update'} for prod in data]

##Temporary
up = [{"_id": prod['prod_id'], "doc_as_upsert": True,  "_type": "product", "_index": "products", "_source": {'doc': prod}, '_op_type': 'index'} for prod in data]


batches = int(math.ceil(len(up)/100.0))
for i in range(0, batches):
    ups = up[i*100:min((i+1)*100, len(up))]
    z = helpers.bulk(es, ups, chunk_size=100)
    print(min((i+1)*100, len(up)))



#####################################################
## Get stuffs from ES
delete_obsolete = True
mining_date_minus_1 = '09/18/2017'

if (delete_obsolete):
    ## Get obsolete date_last_updateds
    dlus = [x['_source']['date_last_updated'] < mining_date_minus_1 for x in hits]
    is_not_recent = numpy.array(hits)[numpy.array(dlus)]

    ## TODO: Fetch and save old products

    ## Delete in ES
    rm_oos = [{"_id": prod['_id'], "_type": "product", "_index": "products", '_op_type': 'delete'} for prod in is_not_recent]

    batches = int(math.ceil(len(rm_oos) / 100.0))
    for i in range(0, batches):
        oos = rm_oos[i * 100:min((i + 1) * 100, len(rm_oos))]
        z = helpers.bulk(es, oos, chunk_size=100)
        print(min((i + 1) * 100, len(rm_oos)))

    ## Delete in Mongo
    client = MongoClient('mongodb://engineering:ZrcyknglNEC1E78KQhI6Q3Y8iWyd4nW7@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
    key = ''
    client = MongoClient('mongodb://glarket:O04vjgawuA6AAHNvX6hZZKsX9nboUI9W@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
    db = client.glarket
    products = db.products
    batches = int(math.ceil(len(is_not_recent) / 50.0))
    for i in range(0, batches):
        delete = is_not_recent[i * 50:min((i + 1) * 50, len(is_not_recent))]
        reqs = [pymongo.DeleteOne({'product_link': x['_source']['product_link']}) for x in delete]
        try:
            result = products.bulk_write(reqs, ordered=False)
            print(result.bulk_api_result)
            print("Batch: " + str(i) + "/" + str(batches) + "; " + str(i / (batches * 1.0) * 100) + "%")
        except BulkWriteError as bwe:
            print(bwe.details)
