#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
import json
from time import sleep

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setTimeout(20)
results = {}
my_file = Path("./pages.json")

if my_file.is_file():    
    print("Opening file")
    results = json.load(open('pages.json'))
        
else:
    print("Requesting data")
    categories = [
            "Landmarks_in_the_United_States_by_state",
            "Tennis",
            "Internet_service_providers",
            "Computer_viruses",
            "Mercedes-Benz",
            "Credit_cards",
            "Fictional_horses",
            "Food_science",
            "French_physicists",
            "Discordianism"]
    
    for cat in categories:
        sparql.setQuery("""
            PREFIX cat: <http://dbpedia.org/resource/Category:>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
            SELECT DISTINCT ?page
            WHERE {
                ?subcat skos:broader* cat:""" + cat + """.
                ?page dcterms:subject ?subcat
            } LIMIT 100
        """)
        
        sparql.setReturnFormat(JSON)
        resultsForOneCat = sparql.query().convert()
        
        if results == {} :
            results = resultsForOneCat
        else :
            results["results"]["bindings"]+=resultsForOneCat["results"]["bindings"]
            
        with open('pages.json', 'w') as fp:
            json.dump(results, fp)


my_file = Path("./pagesWithSubjects.json")

print(results)

if my_file.is_file():    
    print("Opening file")
    data = json.load(open('pagesWithSubjects.json'))
else:
    print("Requesting additionnal data")
    for result in results['results']['bindings']:
        print (result['page']['value'])
        #sleep(0.1)
    
        sparql.setQuery("""
            PREFIX dcterms: <http://purl.org/dc/terms/>
        
            SELECT DISTINCT ?subject
            WHERE {
                <"""+result['page']['value']+"""> dcterms:subject* ?subject
            }
        """)
        sparql.setReturnFormat(JSON)
        subjects = sparql.query().convert()
        subjectList=[]
        for subject in subjects['results']['bindings']:
            subjectList.append(subject['subject']['value'])
            
        subjectList.pop(0)
        result['page']['subjects']=subjectList
        #break
        with open('pagesWithSubjects.json', 'w') as fp:
            json.dump(results, fp)
            
    print('finished')



    
    