'''
Created on Aug 27, 2012

@author: ranjeetbhatia
'''
import BeautifulSoup
from soupselect import select
import urllib2
import time
from pymongo import Connection
import sys

connection=Connection()
styledb=connection.styledb
pins=styledb.pins

def pin_categories():
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen("https://pinterest.com/"))
    cat_list = []
    for c in select(soup, ".submenu a"):
        cat_list.append(c['href'])
    return cat_list

def crawl_pin_category(category):
    #TODO: find next pages
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen("https://pinterest.com/" + category))
    return harvest_pins(soup)
    
def harvest_pins(soup):
    return [p.find("a",{"class":"PinImage ImgLink"})['href'] for p in select(soup, ".pin")]

def grab_pin(pin_id):
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen("https://pinterest.com" + pin_id))
    return {
        "url": select(soup, 'meta[property="og:url"]')[0]['content'],
        "title": select(soup, 'meta[property="og:title"]')[0]['content'],
        "description": select(soup, 'meta[property="og:description"]')[0]['content'],
        "image": select(soup, 'meta[property="og:image"]')[0]['content'],
        "pinboard": select(soup, 'meta[property="pinterestapp:pinboard"]')[0]['content'],
        "pinner": select(soup, 'meta[property="pinterestapp:pinner"]')[0]['content'],
        "source": select(soup, 'meta[property="pinterestapp:source"]')[0]['content'],
        "likes": select(soup, 'meta[property="pinterestapp:likes"]')[0]['content'],
        "repins": select(soup, 'meta[property="pinterestapp:repins"]')[0]['content'],
        "comments": select(soup, 'meta[property="pinterestapp:comments"]')[0]['content'],
        "actions": select(soup, 'meta[property="pinterestapp:actions"]')[0]['content'],
    }
    
while True:
    try:
        time.sleep(1)
        for pin in crawl_pin_category("/all/?category=womens_fashion"):
            time.sleep(1)
            print "total pins downloaded:"+ str(pins.count())
            print "downloading:" + pin
            pin_json=grab_pin(pin)
            if pin_json["source"] and not pins.find_one({'url':pin_json["url"]}):
                pins.save(pin_json)
    except:
    
        print "Unexpected error:", sys.exc_info()[0]
    

        
    


