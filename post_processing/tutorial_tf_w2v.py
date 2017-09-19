##### Tutorial from https://www.tensorflow.org/tutorials/wide

import tempfile
import urllib
import pandas as pd
import tensorflow as tf

## Prepare training and testing data
train_file = tempfile.NamedTemporaryFile()
test_file = tempfile.NamedTemporaryFile()

urllib.urlretrieve("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", train_file.name)
urllib.urlretrieve("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test", test_file.name)

CSV_COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "gender",
    "capital_gain", "capital_loss", "hours_per_week", "native_country",
    "income_bracket"]

## DF of categorial features
df_train = pd.read_csv(train_file.name, names=CSV_COLUMNS, skipinitialspace=True)
df_test = pd.read_csv(test_file.name, names=CSV_COLUMNS, skipinitialspace=True, skiprows=1)

## DF of binary values
train_labels = (df_train["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)
test_labels = (df_test["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)


def input_fn(data_file, num_epochs, shuffle):
  """Input builder function."""
  df_data = pd.read_csv(
      tf.gfile.Open(data_file),
      names=CSV_COLUMNS,
      skipinitialspace=True,
      engine="python",
      skiprows=1)
  # remove NaN elements
  df_data = df_data.dropna(how="any", axis=0)
  labels = df_data["income_bracket"].apply(lambda x: ">50K" in x).astype(int)
  return tf.estimator.inputs.pandas_input_fn(
      x=df_data,
      y=labels,
      batch_size=100,
      num_epochs=num_epochs,
      shuffle=shuffle,
      num_threads=5)

gender = tf.feature_column.categorical_column_with_vocabulary_list(
    "gender", ["Female", "Male"])
occupation = tf.feature_column.categorical_column_with_hash_bucket(
    "occupation", hash_bucket_size=1000)
education = tf.feature_column.categorical_column_with_vocabulary_list(
    "education", [
        "Bachelors", "HS-grad", "11th", "Masters", "9th",
        "Some-college", "Assoc-acdm", "Assoc-voc", "7th-8th",
        "Doctorate", "Prof-school", "5th-6th", "10th", "1st-4th",
        "Preschool", "12th"
    ])
marital_status = tf.feature_column.categorical_column_with_vocabulary_list(
    "marital_status", [
        "Married-civ-spouse", "Divorced", "Married-spouse-absent",
        "Never-married", "Separated", "Married-AF-spouse", "Widowed"
    ])
relationship = tf.feature_column.categorical_column_with_vocabulary_list(
    "relationship", [
        "Husband", "Not-in-family", "Wife", "Own-child", "Unmarried",
        "Other-relative"
    ])
workclass = tf.feature_column.categorical_column_with_vocabulary_list(
    "workclass", [
        "Self-emp-not-inc", "Private", "State-gov", "Federal-gov",
        "Local-gov", "?", "Self-emp-inc", "Without-pay", "Never-worked"
    ])
native_country = tf.feature_column.categorical_column_with_hash_bucket(
    "native_country", hash_bucket_size=1000)

age = tf.feature_column.numeric_column("age")
education_num = tf.feature_column.numeric_column("education_num")
capital_gain = tf.feature_column.numeric_column("capital_gain")
capital_loss = tf.feature_column.numeric_column("capital_loss")
hours_per_week = tf.feature_column.numeric_column("hours_per_week")
age_buckets = tf.feature_column.bucketized_column(
    age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

education_x_occupation = tf.feature_column.crossed_column(
    ["education", "occupation"], hash_bucket_size=1000)
age_buckets_x_education_x_occupation = tf.feature_column.crossed_column(
    [age_buckets, "education", "occupation"], hash_bucket_size=1000)


base_columns = [
    gender, native_country, education, occupation, workclass, relationship,
    age_buckets,
]
crossed_columns = [
    tf.feature_column.crossed_column(
        ["education", "occupation"], hash_bucket_size=1000),
    tf.feature_column.crossed_column(
        [age_buckets, "education", "occupation"], hash_bucket_size=1000),
    tf.feature_column.crossed_column(
        ["native_country", "occupation"], hash_bucket_size=1000)
]

model_dir = tempfile.mkdtemp()
m = tf.estimator.LinearClassifier(
    model_dir=model_dir, feature_columns=base_columns + crossed_columns)