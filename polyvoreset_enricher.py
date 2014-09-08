'''
Created on Aug 21, 2013

@author: ranjeetbhatia


'''

from pymongo import Connection
import sys
import read_properties
import gridfs
from PIL import Image
from StringIO import StringIO
import color_histogram2



connection = Connection()
styledb = connection.stylebot
stylefs=gridfs.GridFS(styledb)
curated_sets=styledb.curated_sets
categories = read_properties.categories()

headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/537 (KHTML, like Gecko) Chrome/28 Safari/537'}



#get all category tree from polyvore for the root category
def enhance_category_list(curated_set):
    for item in curated_set["items"]: 
        if item["category_id"] in categories:
            item["catgeory_list"] = categories[item["category_id"]] 
    curated_set["category_list_enhanced"]=1
    return curated_set

def enhance_image_colors(curated_set):
    for item in curated_set["items"]: 
        if item["imgid"]:
            img = stylefs.get(item["imgid"])
            image = Image.open(StringIO(img.read()))
            print item["imgurl"]
            if color_histogram2.get_colors(image):
                item["top_colors"] = color_histogram2.get_colors(image)[1]
    return curated_set

#loop to process all curated_sets that have been completed
curated_set = True
while curated_set:
    try:
        curated_set = curated_sets.find_one({"$and":[{"complete":1}, {"image_colors_enhanced":{"$exists":False}}]})
        if curated_set: 
            print "procesing set:"+curated_set["id"]
            curated_set = enhance_image_colors(curated_set)
            curated_set["image_colors_enhanced"]=1
            print curated_sets.update({"id":curated_set["id"]},curated_set,safe=True)
    except Exception, info:   
        print sys.exc_info(), info
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)