'''
Created on Aug 13, 2013

@author: ranjeetbhatia
'''
import time
from pymongo import Connection
import sys
import requests
from itertools import chain
import json

connection = Connection()
styledb = connection.stylebot
sets = styledb.sets
curated_sets=styledb.curated_sets
url =  'http://www.polyvore.com/cgi/search.sets?.in=json&.out=json&request={"date":"week","query":"%s","page":%s}'
user_url = 'http://www.polyvore.com/cgi/profile?.in=json&.out=json&request={"id":"%s","page":%s,"filter":"sets"}'
queries = ["sweatshirt", "hoodie","tee","t shirt","tunic","coat","jacket","vest","jeans","pants","leggings","shorts","jumpsuit","romper","boots","clogs","flats","oxfords","pumps","sandals","sneakers","loafers","mocassin","handbags","wallets","messenger","clutches","totes","backpack","Rucksack",]
#users = ["3429964"]
users = ["3429964","4328991","3291531","2874177","3296235","3265576","3045047","3361674","3571862","3211688"]
num_pages = 21
# def download _set(id, url='http://www.polyvore.com/cgi/set.load?.in=json&.out=json&request={"id":"%s"}'):
#   request_url = url % id
#   r = requests.get( request_url )
#   print r
#   if r.status_code == 200:
#     return r.json()["result"]["items"]
#   else:
#     return []


# download JSON of sets matching a query and page number
def download_sets(query, page):
  print "processing", str(query), str(page)
  r = requests.get( url % (query, page))
  return r.json()["result"]["items"] if r.status_code == 200 else []

def download_usersets(query):
  page = 1 
  more_pages = True
  usersets = []
  while more_pages:
    print query, page
    r = requests.get( user_url % (query, page))
    page = page + 1
    usersets.append(r.json()["collections"])
    more_pages = True if r.json()["more_pages"]=="1" else False
  return list(chain(*usersets))
  

#extract the relevant field from each set
def extract_sets(full_set_json,valid_keys=["createdon","clickurl","num_comments","fav_count","title","description","id"]):
  set_json = {k: v for k, v in full_set_json.iteritems() if k in valid_keys}
  return set_json

#saves a given set if it does not exist in the db.
def save_set(polyvore_set):
    if not sets.find_one({'id':polyvore_set["id"]}):
      return sets.save(polyvore_set)  
    else:
      return False   

def save_curatedset(polyvore_set):
    if not curated_sets.find_one({'id':polyvore_set["id"]}):
      print polyvore_set["id"]
      return curated_sets.save(polyvore_set)  
    else:
      return False   

try:
  #loops through queries, then n number of pages and extracts full json, extracts relevant json and then saves each one of them
  #[save_set(extract_sets(full_set_json)) for full_set_json in list(chain(*[download_sets(query,page) for page in range(11,num_pages) for query in queries]))]
  [save_curatedset(extract_sets(full_set_json)) for full_set_json in list(chain(*[download_usersets(user) for user in users]))]
except Exception, info:
    print sys.exc_info(), info
    print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
   

        
    


