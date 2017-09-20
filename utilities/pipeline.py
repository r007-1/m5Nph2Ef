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

fn = "products/outnet_20170919.json"

###### TODO: Figure out file format for each step
###### TODO: Create logs in Sheets


## Check if script is up-to-date


## Mine continuously
#### TODO: Fool-proof in case of connection failure


## Double check format
#### Fix format deficiencies until okay
is_okay = test_format_postmine(fn)
if (not is_okay):
    print('eehhh')

## Add category
def add_main_cat(fn):
    ### DO IN R
    return

fn = fn.replace(".json", "_clean_ld.json")
d = generate_cat(fn)

fn = fn.replace(".json", "_with_cat.json")
is_okay = test_format_postmine(fn)
#### Figure out why prod_id is str!!!!! :(

## Update MongoDB
#### If prod_id exists, update variables
#### Else, upload



## Update ES
#### If prod_id exists, update variables
#### Else, upload

