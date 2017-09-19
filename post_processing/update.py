import elasticsearch
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pymongo import MongoClient
import math
import numpy as np
from collections import Counter
import pandas
from gensim.models import word2vec #docs: https://radimrehurek.com/gensim/models/word2vec.html
import tensorflow as tf

def get_all_vars(var_list):
    es = Elasticsearch('https://elastic:vlox4VZ9OF7aGC01O2lufids@fbc3032a2a91be69517a70b3d75f4eaa.us-east-1.aws.found.io:9243')
    q = 'viglink'
    qq = {
        'from': 0,
        'size': 10000,
        'query': {
            'query_string': {'query': q}
        }
        , "_source": var_list
    }
    r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
    total = r['hits']['total']
    batches = int(math.ceil(total * 1.0 / qq['size']))
    h = []
    for i in range(0, batches):
        if i == 0:
            r = es.search(body=qq, scroll='1m', index='products', doc_type='product')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            h.extend(hits)
            print(len(hits))
        else:
            r = es.scroll(scroll_id=sid, scroll='1m')
            sid = r['_scroll_id']
            hits = r['hits']['hits']
            h.extend(hits)
            print(len(hits))
        print("batch: " + str(i))
    hvar = {}
    df = pandas.DataFrame()
    for var in var_list:
        hvar[var] = [x['_source'][var] for x in h]
    df = pandas.DataFrame(hvar)
    return df




def pred_cat(fn):
sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "post-processing/categorization_091517.ckpt")

m = 'post-processing/w2v_all_091517'
model = word2vec.Word2Vec.load(m)
model_size = 59*250

f = pandas.read_csv(fn)
f = f.replace(np.nan, '', regex=True)
X = prep_X(f)
cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])

x = tf.placeholder(tf.float32, shape=[None, model_size])
y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

W = tf.Variable(tf.zeros([model_size, len(cats)]))
b = tf.Variable(tf.zeros([len(cats)]))

y = tf.matmul(x, W) + b

init = tf.global_variables_initializer()
sess.run(init)


batches = int(math.ceil(len(X)/10000))
y_cat_id = []
y_cat = []
for i in range(batches):
    app_y_cat_id = tf.argmax(y, 1).eval(feed_dict={x:X[i*10000:min((i+1)*10000,len(X)),]})
y_cat_id = tf.argmax(y, 1).eval(feed_dict={x: X_all})
    app_y_cat = [cats[x] for x in y_cat_id]
f = f.assign(cat=y_cat)
    return f

def prep_X(f):
    model_size = 250*59
    model_width = 250
    m = 'post-processing/w2v_all_091517'
    model = word2vec.Word2Vec.load(m)
    cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])
    data = list(f.loc[:, "long_desc_sh"])
    data = [str(x).strip() for x in data]
    sentences = [x.split() for x in data]
    sentences = np.array(sentences)
    n_data = len(sentences)
    X = np.zeros((n_data, model_size))
    invalid = []
    for i in range(0, n_data):
        v = np.zeros(model_size)
        valid_words = 0
        j = 0
        for word in sentences[i]:
            try:
                # v = v + model[word]
                v[j * model_width:(j + 1) * model_width] = model[word]
                valid_words = valid_words + 1
            except:
                pass
            j = j + 1
        if valid_words == 0:
            invalid.append(i)
        else:
            # X_train[i,:] = v/valid_words
            X[i, :] = v
    return X

var_list = ["product_link", "long_desc", "brand"]
df = get_all_vars(var_list)
fn = "post-processing/categorization_all_raw_091517.csv"
df.to_csv(fn, encoding='utf-8')

fn = "post-processing/categorization_all_input_clean_091517.csv"


def nn(X_train, ymat_train):
model_size = 59*250
cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])
graph = tf.Graph()
with graph.as_default():
    x = tf.placeholder(tf.float32, shape=[None, model_size])
    y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

    W = tf.Variable(tf.zeros([model_size, len(cats)]))
    b = tf.Variable(tf.zeros([len(cats)]))

    y = tf.matmul(x, W) + b

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession(graph = graph)
sess.run(tf.global_variables_initializer())

n_data = len(X_train)
batches = int(math.ceil(n_data / 100))
for i in range(0, batches):
    X_batch = X_train[i * 100:min((i + 1) * 100, n_data), ]
    y_batch = ymat_train[i * 100:min((i + 1) * 100, n_data), ]
    train_step.run(feed_dict={x: X_batch, y_: y_batch})

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(accuracy.eval(feed_dict={x: X_train, y_: ymat_train}))