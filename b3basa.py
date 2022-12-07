import requests
from requests.structures import CaseInsensitiveDict

url = "https://xytpiqsykygz2k2wtthklmcu-fast.searchtap.net/v2"

headers = {"authorization": "Bearer 2DYJG7BEJD5BCAW1Q9Z3NLHD"}

data = {"query":"","fields":["*"],"textFacets":["system_producttype","system_vendor","system_availability","option_auto_color","option_auto_size","tags_gender_mhspyaq371nqa9w8y4ab3csl"],"highlightFields":[],"searchFields":["title","description","collections","tags","productType","vendor","variants.sku","sku"],"filter":"priorityScore >= 0 AND publishedTimestamp < 1670436056720 AND publishedTimestamp > 0 AND collectionHandles = \"all-mens-garments-aw22\"  AND in_stock = 1","sort":["-publishedTimestamp"],"skip":39,"count":39,"collection":"RMW65H9J527XMB7EDYAJY11H","facetCount":100,"groupCount":-1,"typoTolerance":1,"textFacetFilters":{"system_producttype":[],"system_vendor":[],"system_availability":[],"price_price_filter":[],"option_auto_color":[],"option_auto_size":[],"tags_gender_mhspyaq371nqa9w8y4ab3csl":[]},"numericFacets":{"price":["[0,100)","[100,200)","[200,300)","[300,400)","[400,500)","[500,2147483647)"]},"numericFacetFilters":{},"textFacetQuery":None,"geo":{}}


resp = requests.post(url, headers = headers, json=data)

print(resp)

