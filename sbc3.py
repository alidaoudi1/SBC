# -*- coding: utf-8 -*-

import json
import csv
import numpy as np
import tensorflow as tf


print("Opening file")
pages = json.load(open('pagesCleaned.json'))

f = csv.writer(open("test.csv", "w",  newline='', encoding='utf-8'))

header = ["pageName"]
for page in pages:
    for propertyName in pages[page]:
        if propertyName not in header:
            header.append(propertyName)
        
f.writerow(header)

for page in pages:   
    line = [None]*len(header)
    line[0] = page
    for propertyName in pages[page]:
        line[[i for i,x in enumerate(header) if x == propertyName].pop(0)] = pages[page][propertyName]        
    f.writerow(line)