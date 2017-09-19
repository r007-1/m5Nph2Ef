import json
import pandas
import math
import datetime
from django.utils import timezone
import shutil
import os

def status(pre):
    photos = pandas.read_json('admin_products/img_1.json')
    p = []
    for photo in range(0, len(photos)):
        p.append(str(photos.loc[photo][0][16:]))
    p.sort()
    for photo in range(0, len(p)):
        if pre == p[photo][0:len(pre)]:
            return photo




