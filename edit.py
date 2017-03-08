import json
import pandas
from presignups_app.models import Product
import math
import datetime
from django.utils import timezone
import numpy

def edit():
    items = pandas.read_json('admin_products/spiders/json/barneys.json')
    prodid = []
    rm = []
    items['date_last_updated'] = ""
    items['on_sale'] = False
    items['merchant'] = "Barney's"
    items['imglink_1'] = ""
    items['imglink_2'] = ""
    items['imglink_3'] = ""
    items['imglink_4'] = ""
    items['imglink_5'] = ""
    items['imglink_6'] = ""
    items['mcat_code'] = ""
    for item in range(0, len(items)):
        if items.loc[item, 'prod_id'] in prodid:
            rm.append(item)
        else:
            prodid.append(items.loc[item, 'prod_id'])
            temp = items['images'][item]
            if temp == []:
                rm.append(item)
            else:
                temp = pandas.DataFrame(items['images'][item])
                tempurls = pandas.DataFrame(items['image_urls'][item])
                for i in range(0, 6):
                    if i < len(items['mcats'][item]):
                        items.loc[item, 'mc_' + str(i + 1)] = items['mcat_' + str(i + 1)][item]
                        if i == (len(items['mcats'][item])-1):
                            items.loc[item, 'mcat_code'] = items['mcat_' + str(i + 1)][item]
                    else:
                        items.loc[item,'mc_' + str(i + 1)] = ""
                for i in range(0, 5):
                    if i < len(temp):
                        items.loc[item, "img_" + str(i+1)] = 'products/photos/' + str(temp['path'][i])[6:]
                        items.loc[item, "imglink_" + str(i+1)] = str(tempurls[0][i])
                    else:
                        items.loc[item, "img_" + str(i+1)] = ""
                        items.loc[item, "imglink_" + str(i+1)] = ""
                if not isinstance(items.loc[item, 'price_sale'], unicode):
                    items.loc[item, 'price_sale'] = 0
                else:
                    try:
                        items.loc[item, 'price_sale'] = int(str(items.loc[item, 'price_sale']).replace(',', ''))
                    except ValueError:
                        items.loc[item, 'price_sale'] = 0
                if not isinstance(items.loc[item, 'price_orig'], unicode):
                    items.loc[item, 'price_orig'] = 0
                else:
                    try:
                        items.loc[item, 'price_orig'] = int(str(items.loc[item, 'price_orig']).replace(',', ''))
                    except ValueError:
                        items.loc[item, 'price_orig'] = 0
                if not isinstance(items.loc[item, 'price_perc_discount'], unicode):
                    items.loc[item, 'price_perc_discount'] = 0
                else:
                    try:
                        items.loc[item, 'price_perc_discount'] = int(str(items.loc[item, 'price_perc_discount']).replace(',', ''))
                    except ValueError:
                        items.loc[item, 'price_perc_discount'] = 0
                if not isinstance(items.loc[item, 'price'], unicode):
                    items.loc[item, 'price'] = 0
                else:
                    try:
                        items.loc[item, 'price'] = int(str(items.loc[item, 'price']).replace(',', ''))
                    except ValueError:
                        items.loc[item, 'price'] = 0
                items.loc[item, 'date_added'] = timezone.now()
                items.loc[item, 'date_last_updated'] = timezone.now()
                items.loc[item, 'is_available'] = True
                items.loc[item, 'price_orig'] = int(items['price_orig'][item])
                items.loc[item, 'price_sale'] = int(items['price_sale'][item])
                items.loc[item, 'price_perc_discount'] = int(items['price_perc_discount'][item])
                items.loc[item, 'price'] = int(items['price'][item])
                items.loc[item, 'tags'] = str(items['tags'][item])
                items.loc[item, 'affiliate_partner'] ="viglink"
                if items.loc[item, 'price'] == items.loc[item, 'price_sale']:
                    items.loc[item, 'on_sale'] = True
                print(str(item) + "saved")
    items = items.drop(items.index[rm])
    z = items.to_csv('admin_products/spiders/json/barneys-021916.csv', index=False)
    print("Done!")
    return items

def rmduplicates():
    items = pandas.read_json('admin_products/spiders/json/barneys.json')
    prodid = []
    rm = [0]
    for item in range(0, len(items)):
        temp = items.loc[item, 'images']
        if temp == []:
            rm.append(item)
        if items.loc[item, 'prod_id'] not in prodid:
            prodid.append(items.loc[item, 'prod_id'])
        else:
            if item not in rm:
                rm.append[item]
        print(item)
    items = items.drop(items.index[rm])
    jsn = items.to_json()
    with open('admin_products/spiders/json/barneys-3.json', 'w') as outfile:
        outfile.write(json.dump(jsn, outfile, indent=4))
    print('done')
