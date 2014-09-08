import requests
import time


f = open("facets.csv", "wb")
# get all facets
facets_response = requests.get("http://api.zappos.com/Search?key=67d92579a32ecef2694b74abfc00e0f26b10d623&list=facetfields")
facets=facets_response.json["facetFields"]
print facets
#lopp through all facets
for i, facet in enumerate(facets): 
	try:
		facet_values_response = requests.get("http://api.zappos.com/Search?key=67d92579a32ecef2694b74abfc00e0f26b10d623&facets="+facet+"&excludes=results")
		time.sleep(0.5)
		facet_values = facet_values_response.json["facets"]
		if len(facet_values) > 0:
			facet_field = facet_values[0]["facetField"]
			facet_display_name = facet_values[0]["facetFieldDisplayName"]
			for values in facet_values[0]["values"]:
				f.write(facet_field.encode("utf-8")+", "+ facet_display_name.encode("utf-8")+", "+ values["name"].encode("utf-8")+", "+values["count"].encode("utf-8")+"\n")
		print "processing facet "+ str(i) +" of "+str(len(facets))
		print facet
	except Exception, e: 
		print str(e)
f.close()


