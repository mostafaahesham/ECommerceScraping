import os
import json
import requests
from math import ceil

availability_aliases = {
    "BACK_SOON":0,
    "COMING_SOON":0,
    "SOLD_OUT":0,
    "HIDDEN":0,
    "SHOW":1
}

pd_file = 'options_sample.json'
with open(pd_file,encoding='UTF-8') as project_file:    
    color = json.load(project_file) 

choice = {
        "sizes": {}
         }

for size in color['sizes']:
    if choice['sizes'][size['name']] in color['sizes'].keys():
        choice["sizes"][size['name']] |= availability_aliases[size['visibilityValue']]
    else:
        choice["sizes"][size['name']] = availability_aliases[size['visibilityValue']]