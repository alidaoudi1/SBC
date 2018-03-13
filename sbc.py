#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:36:39 2018

@author: poste
"""

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import tensorflow as tf
#from rdflib import Graph, URIRef
        
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX cat: <http://dbpedia.org/resource/Category:>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?page
    WHERE {
        ?subcat skos:broader* cat:Landmarks_in_the_United_States_by_state.
        ?page dcterms:subject ?subcat
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
#print(results)

for result in results['results']['bindings']:
    print (result['page']['value'])

    sparql.setQuery("""
        PREFIX dcterms: <http://purl.org/dc/terms/>
    
        SELECT DISTINCT ?subject
        WHERE {
            <"""+result['page']['value']+"""> dcterms:subject* ?subject
        }
    """)
    sparql.setReturnFormat(JSON)
    subjects = sparql.query().convert()
    #print(subjects)
    subjectList=[]
    for subject in subjects['results']['bindings']:
        subjectList.append(subject['subject']['value'])
        
    subjectList.pop(0)
    result['page']['subjects']=subjectList


    #break
    

print('finished')

import json
with open('result.json', 'w') as fp:
    json.dump(results, fp)