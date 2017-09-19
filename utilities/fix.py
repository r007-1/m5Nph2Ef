def convProdIDToStr():
from elasticsearch import Elasticsearch
import json
import math
import pandas
from elasticsearch import helpers
from pymongo import MongoClient
import codecs

    es = Elasticsearch(
        'https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')

    q = 'merchant:Shoptiques'
    qq = {
        'from': 0,
        'size': 10000,
        'query': {
            'query_string': {'query': q}
        }
    }

    r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
    total = r['hits']['total']
    batches = int(math.ceil(total * 1.0 / qq['size']))
    h = list()
    ids = list()

    for i in range(0, batches):
        if i == 0:
            r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            ids.extend(hit['_id'] for hit in hits)
        else:
            r = es.scroll(scroll_id=sid, scroll='1m')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            ids.extend(hit['_id'] for hit in hits)

    si = range(0, len(ids))
    si = [[x] for x in si]

    up = pandas.DataFrame({'sort': si, '_type': 'product', '_id': ids, '_index': 'products', '_op_type': 'delete'})
    up = json.loads(up.to_json(orient='records'))

    for i in range(0, int(math.ceil(len(up) / 20.0))):
        delete = up[i * 20:min((i + 1) * 20, len(up))]
        helpers.bulk(es, delete, chunk_size=20)
        print(min((i + 1) * 20, len(up)))


    ## Delete products in Mongo DB
    client = MongoClient(
        'mongodb://engineering:ZrcyknglNEC1E78KQhI6Q3Y8iWyd4nW7@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
    db = client.glarket
    products = db.products
    rm_st = products.delete_many({"merchant": "Shoptiques"})
    rm_hbx = products.delete_many({"merchant": "HBX"})


    ## Load products with proper prod_id format
    f = 'batch/20170817_st_hbx_2.json'
    c = codecs.open(f, 'r', 'utf-8')
    items = pandas.read_json(c)
    items['prod_id'] = [str(x) for x in items['prod_id']]
    p = json.loads(items.to_json(orient='records'))
    p = p[8379:]
    p = p[82300:]


    ## Upload to ES
    # i=0
    # for element in p:
    #     res = es.index(index='products', doc_type='product', body=element)
    #     print(i)
    #     print(res['created'])
    #     i = i + 1

es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')
for i in range(0, int(math.ceil(len(p) / 100.0))):
    upload = p[i * 100:min((i + 1) * 100, len(p))]
    helpers.bulk(es, upload, chunk_size=100, index='products', doc_type='product')
    print(min((i + 1) * 100, len(p)))


    ## Upload to MongoDB
client = MongoClient(
    'mongodb://engineering:ZrcyknglNEC1E78KQhI6Q3Y8iWyd4nW7@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
db = client.glarket
products = db.products

for i in range(0, int(math.ceil(len(p) / 50.0))):
    upload = p[i * 50:min((i + 1) * 50, len(p))]
    result = products.insert_many(upload)
    print(result)











