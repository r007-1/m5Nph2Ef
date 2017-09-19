import elasticsearch
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pymongo import MongoClient
import math
import numpy
from collections import Counter
import pandas

#https://elasticsearch-py.readthedocs.io/en/master/

from pyelasticsearch import ElasticSearch
from elasticsearch_dsl import Search



## Instantiate ES
es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')


## Get all product links
q = 'viglink'
qq = {
    'from': 0,
    'size': 10000,
    'query': {
        'query_string': {'query': q}
    }
    ,"_source": ["product_link", "prod_id", "brand"]
}

plinks = list()
ids = list()
pids = list()
brands = list()
r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
total = r['hits']['total']
batches = int(math.ceil(total*1.0/qq['size']))


#rr = [x['_source'] for x in r['hits']['hits']]


for i in range(0, batches):
    if i==0:
        r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
        sid = r['_scroll_id']
        hits = r['hits']['hits']
        brands.extend([hit['_source']['brand'] for hit in hits])
        # plinks.extend([hit['_source']['product_link'] for hit in hits])
        # ids.extend(hit['_id'] for hit in hits)
        # pids.extend([hit['_source']['prod_id'] for hit in hits])
    else:
        r = es.scroll(scroll_id=sid, scroll='1m')
        sid = r['_scroll_id']
        hits = r['hits']['hits']
        brands.extend([hit['_source']['brand'] for hit in hits])
        # plinks.extend([hit['_source']['product_link'] for hit in hits])
        # ids.extend(hit['_id'] for hit in hits)
        # pids.extend([hit['_source']['prod_id'] for hit in hits])


plinkses = plinks
idses = ids
pidses = pids

## Identify duplicates
idsa = numpy.array(ids)
plinksa = numpy.array(plinks)

il = pandas.DataFrame({'id': ids, 'plink': plinks, 'pid': pids})

uplinksa = numpy.unique(plinksa)
dids = []


c = Counter(plinksa)
ck = c.keys()
cv = c.values()
di = numpy.where(numpy.array(cv)>1)[0]
oi = numpy.where(numpy.array(cv)==1)[0]

## Get links and ids of valid items
olinks = numpy.array(ck)[oi.tolist()].tolist()
oids = list(il['id'][il['plink'].isin(olinks)])
oids_es = oids

## Get ids of valid duplicates
vdlinks = numpy.array(ck)[di.tolist()].tolist()
alld = il[il['plink'].isin(vdlinks)]
alldids = list(alld['id'])
vdids = list(alld.drop_duplicates(subset=['plink'])['id'])
vdids_es = vdids

## Compile uploaded links
uploaded = []
uploaded.extend(oids_es)
uploaded.extend(vdids_es)
uploaded_es = uploaded
up_pid_es = list(il['pid'][il['id'].isin(uploaded_es)])


## Get ids of invalid duplicates
idids = list(set(alldids) - set(vdids))
idids_es = idids


## Delete invalid duplicates in elasticsearch
## TODO

si = range(0, len(idids_es))
si = [[x] for x in si]

up = pandas.DataFrame({'sort': si, '_type': 'product', '_id': idids_es, '_index': 'products', '_op_type': 'delete'})
up = json.loads(up.to_json(orient='records'))

for i in range(0, int(math.ceil(len(up)/100.0))):
    delete = up[i*100:min((i+1)*100, len(up))]
    helpers.bulk(es, delete, chunk_size=100)
    print(min((i+1)*100, len(up)))

#es.delete(index="products",doc_type="product",id=r['_id'])
#helpers.bulk(es, delete(), chunk_size=50, index='products', doc_type='product')



## Load recent mined products
file = 'batch/2017-08-09.json'
f = open(file, 'r')
ff = json.load(f)
j = ff


## Get the list of unuploaded products
# Get ids of j
products = pandas.DataFrame(j)
links = list(products['product_link'])
lds = list(products['long_desc'])
#ulinks = list(set(links) - set(uploaded))
il = pandas.DataFrame({'id': products['prod_id'], 'plink': products['product_link']})

## Check duplicates
c = Counter(links)
ck = c.keys()
cv = c.values()
di = numpy.where(numpy.array(cv)>1)[0]
oi = numpy.where(numpy.array(cv)==1)[0]


## Get links and ids of valid items
olinks = numpy.array(ck)[oi.tolist()].tolist()
oids = list(il['id'][il['plink'].isin(olinks)])


## Get ids of valid duplicates
vdlinks = numpy.array(ck)[di.tolist()].tolist()
alld = il[il['plink'].isin(vdlinks)]
alldids = list(alld['id'])
vdids = list(alld.drop_duplicates(subset=['plink'])['id'])


## Get ids of invalid duplicates ##TODO
idids = list(set(alldids) - set(vdids))


## Remove invalid duplicates
products = products[~products['prod_id'].isin(idids)]


# Remove uploaded ids #TODO
products = products[~products['prod_id'].isin(up_pid_es)]


##TODO Make sure product ids and product links are unique!!!!! GUHGHGHG


## Upload missing products
p = json.loads(products.to_json(orient='records'))
for element in p:
    del element['']

i=0
for element in p:
    res = es.index(index='products', doc_type='product', body=element)
    print(i)
    print(res['created'])
    i = i + 1



### Normal upload
## A
helpers.bulk(es, p, chunk_size=50, index = 'products', doc_type='product')
## B
helpers.bulk(es, j, chunk_size=50)
## C
for i in range(0, int(math.ceil(len(j)/100.0))):
    upload = j[i*100:min((i+1)*100, len(j))]
    helpers.bulk(es, upload, chunk_size=100)
    print(min((i+1)*100, len(j)))


#https://api.mongodb.com/python/current/tutorial.html
#j = j[239907:]

client = MongoClient('mongodb://engineering:ZrcyknglNEC1E78KQhI6Q3Y8iWyd4nW7@ds119030-a0.mlab.com:19030,ds119030-a1.mlab.com:19030/glarket?replicaSet=rs-ds119030')
db = client.glarket
products = db.products

for i in range(0, int(math.ceil(len(j)/50.0))):
    upload = j[i*50:min((i+1)*50, len(j))]
    result = products.insert_many(upload)
    print(result)






#oids = [idlink.keys()[idlink.values().index(x)] for x in olinks]
#oids = [k for k,v in idlink.iteritems() if v in olinks]
#vdids = [idlink.keys()[idlink.values().index(x)] for x in vdlinks] ##find first key ##takes forever


##TODO
#1 Run ES duplicate script
#2 Delete duplicates
#3 Run mined product script
#4 Reupload missing products
#5 Test



#
#
# for i in range(0, batches):
#     qq = {
#         'from': 10000*i,
#         'size': 10000,
#         'query': {
#             'query_string': {'query': q}
#         },
#     }
#     r = es.search(body=qq)
#     plinks.append(r['hits']['hits'])
#
#
# es.search()
# es.search(index='products', doc_type='product', body='viglink')



### Find rounded-up product IDs
pids = list(products["prod_id"])
plinks = list(products["product_link"])
lp = pandas.DataFrame({'plink': plinks, 'pid': pids})
last = [str(x)[-4:] for x in pids]
numpy.where(numpy.array(last)='0000')

c = Counter(last)
cv = c.values()
ck = c.keys()




### UPDATE
es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')


## Get all product links
q = 'merchant: HBX'
qq = {
    'from': 0,
    'size': 10000,
    'query': {
        'query_string': {'query': q}
    }
    ,"_source": ["on_sale"]
}

h = list()
r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
total = r['hits']['total']
batches = int(math.ceil(total*1.0/qq['size']))


#rr = [x['_source'] for x in r['hits']['hits']]

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

true = [x for x in h if x['_source']['on_sale']==1]
false = [x for x in h if x['_source']['on_sale']==False]

for i in range(0, len(h)):
    os = h[i]['_source']['on_sale']
    if os:
        h[i]['_source']['on_sale'] = int(os == True)
    else:
        h[i]['_source']['on_sale'] = int(os == True)

up = [ {'_id': result['_id'], "_type": "product", "_index": "products", "_source": {'doc': result['_source']}, '_op_type': 'update'} for result in h]

for i in range(0, int(math.ceil(len(up)/100.0))):
    delete = up[i*100:min((i+1)*100, len(up))]
    helpers.bulk(es, delete, chunk_size=100)
    print(min((i+1)*100, len(up)))