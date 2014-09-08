'''
Created on Aug 21, 2013

@author: ranjeetbhatia
'''

from pymongo import Connection
import sys
import time
import requests
from bson.binary import Binary
import gridfs
import random


connection = Connection()
styledb = connection.stylebot
stylefs=gridfs.GridFS(styledb)
curated_sets=styledb.curated_sets
set_url = 'https://www.polyvore.com/cgi/set.load?.in=json&.out=json&request={"id":"%s"}'
item_url = 'https://www.polyvore.com/cgi/thing?.in=json&.out=json&request={"id":"%s"}'

headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/537 (KHTML, like Gecko) Chrome/28 Safari/537'}


def expand_item_details(item):
    time.sleep(random.randint(1,5))
    print " procesing item:"+item["thing_id"]
    r = requests.get( item_url % item["thing_id"],headers=headers)
    valid_keys =["description","category_id","thing_id","title","imgurl","is_product","is_shop_category","url","brand","branded_title","is_commercial"]
    #get all things and the category id
    item = {k:v for (k, v) in r.json()["thing"].iteritems() if k in valid_keys} 
    img_binary=Binary(requests.get(item["imgurl"]).content)
    item["imgid"]=stylefs.put(img_binary)
    return item

def expand_curated_set(curated_set):
    time.sleep(random.randint(1,5))
    r = requests.get( set_url % curated_set["id"],headers=headers)
    curated_set["user_name"] = r.json()["collection"]["user_name"]
    curated_set["user_id"] = r.json()["collection"]["user_id"]
    valid_keys =["thing_id","category_id"]
    #get all things and the category id
    items = [{k:v for (k, v) in item.iteritems() if k in valid_keys} for item in r.json()["collection"]["items"] if "thing_id" in item ]
    curated_set["items"] = [expand_item_details(item) for item in items]
    return curated_set


#loop to process all curated_sets
curated_set = True
while curated_set:
    try:
        time.sleep(random.randint(1,5))
        curated_set = curated_sets.find_one({"complete":{"$exists":False}})
        if curated_set: 
            print "procesing set:"+curated_set["id"]
            curated_set = expand_curated_set(curated_set)
            curated_set["complete"]=1
            print curated_sets.update({"id":curated_set["id"]},curated_set,safe=True)
    except Exception, info:   
        print sys.exc_info(), info
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)