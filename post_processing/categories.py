## Load libraries
import tensorflow as tf
import pandas as p
from gensim.models import word2vec #docs: https://radimrehurek.com/gensim/models/word2vec.html
import gensim
import numpy as np
import math
import random

## Load data
f = p.read_csv("post_processing/cat_tr_t_raw_Xy_50w.csv")
f = f.replace(np.nan, '', regex=True) #Replace nan values with ""

fn = "post_processing/categorization_all_input_clean_091517.csv"
f = p.read_csv(fn)

data = list(f.loc[:,"long_desc_sh"]) ####??? ##TODO
data = [str(x).strip() for x in data]


sentences = [x.split() for x in data]
model = word2vec.Word2Vec(sentences, min_count=25, window=3, size=250, workers=4, iter=50, sg=0)
m = 'post_processing/w2v_all_091517'
model.save(m)




###########################


m = 'post_processing/w2v_50k_sh'
m = 'post_processing/w2v_all_091517'
model = word2vec.Word2Vec.load(m)

words_max = 59
model_width=250
model_size = model_width*words_max
random.seed(91517)
rands = random.sample(range(len(data)), len(data))
training_indices = rands[0:15000]
testing1_indices = rands[15000:16000]
testing2_indices = rands[16000:17000]
testing3_indices = rands[17000:18000]
validation_indices = rands[18000:20000]

sentences = np.array(sentences)
yraw = f.loc[:,"cat"]
cats = np.array(['beauty & health', 'electronics', 'home', 'kids', 'men', 'men & women', 'others', 'women'])

def load_data(sentences, yraw, indices):
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

X_train, ymat_train = load_data(sentences, yraw, training_indices)

import tensorflow as tf
saver = tf.train.Saver(max_to_keep=1)

x = tf.placeholder(tf.float32, shape=[None, model_size])
y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

W = tf.Variable(tf.zeros([model_size, len(cats)]))
b = tf.Variable(tf.zeros([len(cats)]))

y = tf.matmul(x, W) + b

#with tf.Session() as sess:
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

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


X_train, ymat_train = load_data(sentences, yraw, testing1_indices)


y_cat_id = tf.argmax(y,1).eval(feed_dict={x: X_all})
y_cat = [cats[x] for x in y_cat_id]

indices = training_indices
d = p.DataFrame(f.loc[indices,"product_link"])
d = d.assign(cat=y_cat)

saver = tf.train.Saver(max_to_keep=1)




x = tf.placeholder(tf.float32, shape=[None, model_size])
y_ = tf.placeholder(tf.float32, shape=[None, len(cats)])

W = tf.Variable(tf.zeros([model_size, len(cats)]))
b = tf.Variable(tf.zeros([len(cats)]))

y = tf.matmul(x, W) + b
y = tf.nn.softmax(tf.matmul(x, W) + b)


X_train, ymat_train = load_data(sentences, yraw, testing1_indices)




feed_dict = {x: X_train}
classification = sess.run(y, feed_dict)
print classification

sess.run(tf.argmax(y, 1), feed_dict={x: X_train})











##########


X_train, ymat_train = load_data(sentences, yraw, testing1_indices)
print(accuracy.eval(feed_dict={x: X_train, y_: ymat_train}))


fd={x: X_train, y_: ymat_train}



W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64]) ##TODO
b_conv2 = bias_variable([64]) ##TODO

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024]) ##TODO
b_fc1 = bias_variable([1024]) ##TODO

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
      train_accuracy = accuracy.eval(feed_dict={
          x: batch[0], y_: batch[1], keep_prob: 1.0})
      print('step %d, training accuracy %g' % (i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

  print('test accuracy %g' % accuracy.eval(feed_dict={
      x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))









def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
