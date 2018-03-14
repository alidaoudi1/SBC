# -*- coding: utf-8 -*-

import json
from SPARQLWrapper import SPARQLWrapper, JSON

'''
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setTimeout(600)


sparql.setQuery("""
            PREFIX cat: <http://dbpedia.org/resource/Category:>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  
            SELECT DISTINCT ?page ?property ?value
            WHERE {
                ?subcat skos:broader* cat:Tennis.
                ?page dcterms:subject ?subcat.
                ?page rdf:type dbo:Person.
                ?page ?property ?value.
            } 
ORDER BY DESC(?page)
LIMIT 3000
        """)

sparql.setReturnFormat(JSON)
result = sparql.query().convert()
'''

print("Opening file")
result = json.load(open('pages2.json'))

pages = result["results"]["bindings"]
pagesCleaned = {}
for page in pages:
    pageName = page["page"]["value"]
    propertyName = page["property"]["value"]
    propertyValue = page["value"]["value"]
    
    if pageName not in pagesCleaned:
        pagesCleaned[pageName] = {}
    

    if propertyName in pagesCleaned[pageName]:
        pagesCleaned[pageName][propertyName].append(propertyValue)
    else:    
        pagesCleaned[pageName][propertyName] = [propertyValue]
     
        
pagesCleaned.pop(pageName)   

with open('pagesCleaned.json', 'w') as fp:
    json.dump(pagesCleaned, fp)     