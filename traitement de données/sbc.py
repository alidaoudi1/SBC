#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
import json

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


my_file = Path("./pagesWithSubjectsAndLinks.json")

print(results)

if my_file.is_file():    
    print("Opening file")
    results = json.load(open('pagesWithSubjectsAndLinks.json'))
else:
    print("Requesting additionnal data")
    for result in results['results']['bindings']:
        print (result['page']['value'])
        #sleep(0.1)
    
        sparql.setQuery("""
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX onto: <http://dbpedia.org/ontology/>
        
            SELECT DISTINCT ?subject ?linkedTo
            WHERE {
                <"""+result['page']['value']+"""> dcterms:subject* ?subject.
                <"""+result['page']['value']+"""> onto:wikiPageExternalLink ?linkedTo
                
            }
        """)
        sparql.setReturnFormat(JSON)
        subjects = sparql.query().convert()
        print(subjects)
        subjectList=[]
        for subject in subjects['results']['bindings']:
            subjectList.append(subject['subject']['value'])
            
        subjectList.pop(0)
        result['page']['subjects']=subjectList
        #break
        with open('pagesWithSubjectsAndLinks.json', 'w') as fp:
            json.dump(results, fp)
            
    print('finished')


pages = results['results']['bindings']
sample = [421, 272, 922, 873, 359, 962, 33, 592, 112, 471, 256, 566, 621, 219, 301, 547, 537, 851, 135, 451, 464, 535, 2, 394, 218, 492, 351, 258, 625, 191, 624, 698, 466, 858, 298, 455, 556, 668, 832, 461, 404, 608, 321, 26, 164, 5, 773, 23, 780, 884, 511, 936, 814, 389, 247, 716, 482, 25, 665, 89, 641, 73, 259, 197, 616, 793, 314, 683, 95, 234, 754, 257, 601, 199, 309, 855, 766, 407, 59, 216, 622, 124, 427, 281, 559, 682, 286, 58, 75, 903, 679, 305, 296, 712, 12, 913, 362, 348, 688, 227, 799, 405, 245, 720, 76, 831, 452, 200, 369, 961, 750, 99, 696, 502, 277, 211, 635, 207, 228, 269, 312, 852, 549, 275, 724, 804, 386, 261, 445, 965, 861, 387, 660, 406, 900, 534, 593, 911, 753, 370, 53, 484, 499, 536, 700, 510, 190, 591, 57, 295, 870, 819, 311, 80, 181, 384, 763, 659, 366, 467, 134, 32, 632, 302, 332, 491, 428, 415, 274, 24, 739, 130, 8, 797, 838, 87, 912, 475, 19, 906, 945, 631, 107, 857, 330, 781, 844, 437, 329, 937, 46, 334, 171, 500, 676, 934, 98, 339, 940, 230, 795, 479, 304, 636, 128, 730, 826, 113, 835, 589, 179, 264, 168, 364, 649, 434, 11, 860, 489, 108, 671, 806, 571, 575, 174, 713, 267, 365, 317, 323, 798, 619, 617, 596, 562, 308, 236, 885, 121, 444, 736, 842, 166, 623, 910, 137, 528, 946, 935, 402, 439, 92, 544, 473, 662, 647, 845, 60, 715, 823, 778, 83, 385, 222, 876, 167, 706, 375, 116, 577, 692, 422, 265, 891, 320, 221, 486, 843, 169, 188, 198, 159, 917, 303, 43, 240, 74, 496, 521, 241, 782, 745, 142, 131, 355, 514, 440, 17, 106, 64, 765, 674, 833, 588, 65, 602, 300, 469, 655, 789, 331, 597, 709, 749, 531, 895, 882, 371, 790, 743, 630, 802]

for index in sample:
    print(pages[index])