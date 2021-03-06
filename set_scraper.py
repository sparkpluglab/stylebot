'''
Created on Aug 27, 2012

@author: ranjeetbhatia
'''
import BeautifulSoup
from soupselect import select
import time
from pymongo import Connection
import sys
import re
import requests
from bson.binary import Binary
import gridfs



#URL to only pick relevant pins
regx=re.compile("polyvore.*/set\?",re.IGNORECASE)


# get items and item details for a set with url
def get_sets_json(url):
    print "processing set:" +url
    soup = BeautifulSoup.BeautifulSoup(requests.get(url).content)
    set_json={}
    set_json["url"]=url
    items=select(soup, 'div[id="items"] div[class~="item"]')
    # for each item get get items and append
    if len(items)==0: return False
    # find sets likes and views
    set_json["likes"] = int(select(soup, 'meta[property="polyvore:likes"]')[0]['content'])
    try:
        set_json["views"] = int(soup.find(text=re.compile(r'(.*) views',re.IGNORECASE)).encode().split('.')[1].split()[0].replace(',',''))
    except (IndexError, AttributeError) as e:
        print e
    except ValueError as e:
        set_json["views"] = 5


    #get related styles at the bottom right of page for a set
    try:
        set_json["styles"] = list(style.text for style in soup.find(text='Related Styles').parent.parent.parent.findAll('a'))
    except (AttributeError, IndexError) as e:
        print e
        return {}
    set_json["items"] = []
    #extract all items in the set
    
    for item in items:
        time.sleep(2)
        item_url = "http://www.polyvore.com"+item.a["href"][2:]
        item_json=get_item(item_url)
        if item_json==False:return {}
        #only add relevant items that have the top crumb information otherwise they are just pictures
        if item_json["crumbs"]!=[]:
            set_json["items"].append(item_json)
    return set_json

#get item details
def get_item(item_url):
    print "processing item:"+item_url
    soup = BeautifulSoup.BeautifulSoup(requests.get(item_url).text)
    if len(select(soup, 'h1[title]'))==0:return False
    #extract the item info
    item_json={
               "url":item_url,
               "name":select(soup, 'h1[title]')[0].text,
               "description": select(soup, 'div[class="tease"]')[0].text if select(soup, 'div[class="tease"]') else "",
               "img_url":select(soup, 'center[id="thing_img"]')[0].a.img["src"] if select(soup, 'center[id="thing_img"]') else '',
               "crumbs":list(crumb.a.text for crumb in soup.findAll('span','crumb')),
               "source":select(soup, 'div[id="price_and_link"] a')[0].text if select(soup, 'div[id="price_and_link"] a') else '',
               "likes":int(select(soup, 'meta[property="polyvore:saves"]')[0]['content']),
               }
    #get categories
    if soup.find(text='Shop categories'):
        item_json["categories"]=list(category.text for category in soup.find(text='Shop categories').parent.parent.parent.findAll('a',"hover_clickable") ) 
    #download img if the item as crumbs otherwise it is just a picture
    if item_json["crumbs"]!=[]:
        img_binary=Binary(requests.get(item_json["img_url"]).content)
        #item_json["img_id"]=stylefs.put(img_binary)
    print item_json
    return item_json


