import json
import pandas
import math
import datetime
from django.utils import timezone
import shutil
import os

def move_files():
    photos = pandas.read_json('admin_products/img_1.json')
    e = []
    cwd = os.getcwd()
    for photo in range(0, len(photos)):
        file = unicode(photos.loc[photo][0][16:])
        src = '/admin_products/products/'
        dest = '/s3-static/products/photos/'
        try:
            src_path = os.path.join(src, file)
            dest_path = os.path.join(dest, file)
            os.rename(src_path, dest_path)
        except Exception as ex:
            e.append(photo)
        print(photo)
    print("Done!!!")
    return e