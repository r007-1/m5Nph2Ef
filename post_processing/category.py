## Load libraries
import tensorflow as tf
import pandas as p
from gensim.models import word2vec #docs: https://radimrehurek.com/gensim/models/word2vec.html
import gensim
import numpy as np
import math
import random
import json

### TO DO
def train_w2v():
    return

def train_cat_nn():
    fn = "post_processing/cat_tr_t_raw_Xy_50w.csv"
    f = p.read_csv(fn)
    f = f.replace(np.nan, '', regex=True)  # Replace nan values with ""

    data = list(f.loc[:, "long_desc_sh"])  ####??? ##TODO
    data = [str(x).strip() for x in data]
    sentences = [x.split() for x in data]

    m = 'post_processing/w2v_all_091517'
    model = word2vec.Word2Vec.load(m)

    words_max = 59
    model_width = 250
    model_size = model_width * words_max
    random.seed(91517)
    rands = random.sample(range(len(data)), len(data))
    training_indices = rands[0:15000]
    testing1_indices = rands[15000:16000]
    testing2_indices = rands[16000:17000]
    testing3_indices = rands[17000:18000]
    validation_indices = rands[18000:20000]

    sentences_train = np.array(sentences)
    yraw = f.loc[:, "cat"]
    cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])

    X_train, ymat_train = load_data(sentences_train, yraw, training_indices)

    x = tf.placeholder(tf.float32, shape=[None, model_size])
    y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

    W = tf.Variable(tf.zeros([model_size, len(cats)]))
    b = tf.Variable(tf.zeros([len(cats)]))

    y = tf.matmul(x, W) + b

    # with tf.Session() as sess:
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver(max_to_keep=1)

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))

    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    n_data = len(X_train)
    batches = int(math.ceil(n_data / 100))

    for i in range(0, batches):
        X_batch = X_train[i * 100:min((i + 1) * 100, n_data), ]
        y_batch = ymat_train[i * 100:min((i + 1) * 100, n_data), ]
        train_step.run(feed_dict={x: X_batch, y_: y_batch})

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(accuracy.eval(feed_dict={x: X_train, y_: ymat_train}))

    savePath = saver.save(sess, 'post_processing/categorization_091517.ckpt')
    return

def generate_cat(fnn):
    fn = fnn
    f = p.read_json(fn)
    f = f.replace(np.nan, '', regex=True)  # Replace nan values with ""

    data = list(f.loc[:, "long_desc_sh"])
    data = [str(x).strip() for x in data]
    sentences = [x.split() for x in data]

    m = 'post_processing/w2v_all_091517'
    model = word2vec.Word2Vec.load(m)

    what = "lauroyl"
    z = ["lauroyl" in x for x in sentences]
    keep = ["lauroyl" not in x for x in sentences]
    whazt = np.array(range(len(sentences)))[np.array(z)]
    s = np.array(sentences)[np.array(keep)]

    X_all = load_X_all(s, model)

    ######################################################################
    fn = "post_processing/cat_tr_t_raw_Xy_50w.csv"
    f = p.read_csv(fn)
    f = f.replace(np.nan, '', regex=True)  # Replace nan values with ""

    data = list(f.loc[:, "long_desc_sh"])  ####??? ##TODO
    data = [str(x).strip() for x in data]
    sentences = [x.split() for x in data]

    m = 'post_processing/w2v_all_091517'
    model = word2vec.Word2Vec.load(m)

    words_max = 59
    model_width = 250
    model_size = model_width * words_max
    random.seed(91517)
    rands = random.sample(range(len(data)), len(data))
    training_indices = rands[0:15000]
    testing1_indices = rands[15000:16000]
    testing2_indices = rands[16000:17000]
    testing3_indices = rands[17000:18000]
    validation_indices = rands[18000:20000]

    sentences_train = np.array(sentences)
    yraw = f.loc[:, "cat"]
    cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])

    X_train, ymat_train = load_data(sentences_train, yraw, training_indices)

    x = tf.placeholder(tf.float32, shape=[None, model_size])
    y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

    W = tf.Variable(tf.zeros([model_size, len(cats)]))
    b = tf.Variable(tf.zeros([len(cats)]))

    y = tf.matmul(x, W) + b

    # with tf.Session() as sess:
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver(max_to_keep=1)

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))

    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    n_data = len(X_train)
    batches = int(math.ceil(n_data / 100))

    for i in range(0, batches):
        X_batch = X_train[i * 100:min((i + 1) * 100, n_data), ]
        y_batch = ymat_train[i * 100:min((i + 1) * 100, n_data), ]
        train_step.run(feed_dict={x: X_batch, y_: y_batch})

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(accuracy.eval(feed_dict={x: X_train, y_: ymat_train}))

    ######################################################################

    y_cat_id = np.zeros(len(X_all))
    batches = int(math.ceil(len(X_all)/10000))

    for b in range(batches):
        r = range(b*10000, min((b+1)*10000,len(X_all)))
        y_cat_id[r] = tf.argmax(y, 1).eval(feed_dict={x: X_all[r,:]})

    y_cat = [cats[int(x)] for x in y_cat_id]

    fn = fnn
    f = p.read_json(fn)
    f = f.replace(np.nan, '', regex=True)

    f = f.loc[keep,:] ##### Check later TODO
    f = f.assign(cat_1=y_cat)
    f = f.drop("long_desc_sh", 1)

    z = json.loads(f.to_json(orient='records'))
    fn = fn.replace(".json", "") + "_with_cat.json"
    with open(fn, 'w') as outfile:
        json.dump(z, outfile)
    return z


########### HELPER FUNCTIONS ######################
def load_data(sentences, yraw, indices):
    words_max = 59
    model_width = 250
    model_size = model_width * words_max

    cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])
    training = sentences[indices]
    yraw_train = yraw[indices]
    ymat_train = np.zeros((len(indices), len(cats)))
    for i in range(0, len(cats)):
        ymat_train[:, i] = ((yraw_train == cats[i]) + 0)

    X_train = np.zeros((len(indices), model_size))
    invalid = []

    for i in range(0, len(training)):
        v = np.zeros(model_size)
        valid_words = 0
        j = 0
        for word in training[i]:
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
            X_train[i, :] = v
    return X_train, ymat_train




def load_X_all(sentences, model):
    words_max = 59
    model_width = 250
    model_size = model_width*words_max

    indices = range(len(sentences))
    X_all = np.zeros((len(indices), model_size))
    invalid = []

    for i in range(0, len(sentences)):
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
            X_all[i, :] = v
    return X_all