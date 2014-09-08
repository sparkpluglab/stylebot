
#open 
FACETS = "zappos_relevant_facets"
CATEGORIES = "polyvore_categories"
CATEGORIES_TO_FACETS = "category_to_facets"

def facets():
	#reads the files and returns facet_header:[list of facet values]
	f = open(FACETS, "r")
	facets = {}
	for row in f.readlines():
		columns = row.split(",")
		facet_heading = columns[0]
		if facet_heading not in facets:
			facets[facet_heading] = []
		facets[facet_heading].append(columns[2])
		print "-1," + facet_heading + "_" + columns[2].strip().replace(" ","") + "," + facet_heading + "," + columns[2]
	return facets
	f.close()


def categories():
	# reads the categories and retruns category id :{dictionary of category tree}
	f = open(CATEGORIES, "r")
	categories = {}
	for row in f.readlines():
		columns = row.strip().split(",")
		#print columns
		category_id = columns[0].split(":")[0]
		if category_id not in categories:
			categories[category_id] = {}
			columns.reverse()
		for  i, category in enumerate(columns):
			#print category_id
			#print i
			categories[category_id]["p%i" %i] = {}
			categories[category_id]["p%i" %i]["id"] = columns[i].split(":")[0]
			categories[category_id]["p%i" %i]["name"] = columns[i].split(":")[1]
			
			# just some utility code to flatten the features - may not use again
			if i == 1 and len(columns) == 2: #only get category such as tops etc. i.e. second level
				print categories[category_id]["p%i" %i]["id"]+ "," +   categories[category_id]["p0"]["name"] + \
				"_" + categories[category_id]["p%i" %i]["name"] + "," + categories[category_id]["p0"]["name"] + \
				"," + categories[category_id]["p%i" %i]["name"]

	return categories
	f.close()

def categories_to_facets():
	#reads the files and returns facet_header:[list of facet values]
	f = open(CATEGORIES_TO_FACETS, "r")
	categories_to_facets = {}
	for row in f.readlines():
		columns = row.strip().split(":")
		category_id = columns[0]
		if category_id not in categories_to_facets:
			categories_to_facets[category_id] = []
		for facet in columns[1].split(","):
			categories_to_facets[category_id].append(facet)
	return categories_to_facets
	f.close()
facets()