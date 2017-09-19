from algoliasearch import algoliasearch
import os
import csv

#setwd to to ~/Documents/nuylkr

def resume_saving():
    f = open("sample.csv", "r")
    batch = csv.reader(f)
    client = algoliasearch.Client("BTPCHYHQQY", "1f86acd5ce887ec4c6c7b57e660680da")
    index = client.initIndex("products")
    count = 0
    table = []
    for row in batch:
        if count == 0:
            labels = row
        else:
            product = {}
            for i in range(0,len(labels)):
                product[labels[i]] = row[i]
            table.append(product)
            break
        count += 1

