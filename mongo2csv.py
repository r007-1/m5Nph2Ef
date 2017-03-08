from pymongo import MongoClient
import pandas
import json
from bson.json_util import dumps

client = MongoClient('mongodb://read:uG1R136m@ds023329-a0.mlab.com:23329/nuyolk?replicaSet=rs-ds023329')
products = client.nuyolk.products
results = products.find({ "prod_id": { "$gt": 0 } }, { "prod_id": 1, "brand": 1, "short_desc": 1})
results = products.find({ "mcat_1": {"$ne": ""} }, { "mcat_1": 1, "mcat_2": 1, "mcat_": 1})

json = dumps(results)
p = pandas.read_json(json)

p.to_csv("R-scripts/raw/product-urls-raw.csv", encoding='utf-8')


def mongo2csv(filename)
    p = pandas.read_json(filename)
    p.to_csv(filename.replace(".json", ".csv"), encoding='utf-8')
    print "done"
