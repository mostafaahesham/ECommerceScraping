import requests
from requests.structures import CaseInsensitiveDict

url = "https://xytpiqsykygz2k2wtthklmcu-fast.searchtap.net/v2"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json, text/plain, */*"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Accept-Language"] = "en-US,en;q=0.9"
headers["authorization"] = "Bearer 2DYJG7BEJD5BCAW1Q9Z3NLHD"
headers["Connection"] = "keep-alive"
headers["Content-Length"] = "968"
headers["Content-Type"] = "application/json"
headers["Host"] = "xytpiqsykygz2k2wtthklmcu-fast.searchtap.net"
headers["Origin"] = "https://dalydress.com"
headers["Referer"] = "https://dalydress.com/"
headers["sec-ch-ua"] = ""Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24""
headers["sec-ch-ua-mobile"] = "?0"
headers["sec-ch-ua-platform"] = ""Linux""
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "cross-site"
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

data = '{"query":"","fields":["*"],"textFacets":["system_producttype","system_vendor","system_availability","option_auto_color","option_auto_size","tags_gender_mhspyaq371nqa9w8y4ab3csl"],"highlightFields":[],"searchFields":["title","description","collections","tags","productType","vendor","variants.sku","sku"],"filter":"priorityScore >= 0 AND publishedTimestamp < 1669831286367 AND publishedTimestamp > 0 AND collectionHandles = \"mens-t-shirts-fw22\"  AND in_stock = 1","sort":["-publishedTimestamp"],"skip":0,"count":24,"collection":"RMW65H9J527XMB7EDYAJY11H","facetCount":100,"groupCount":-1,"typoTolerance":1,"textFacetFilters":{"system_producttype":[],"system_vendor":[],"system_availability":[],"price_price_filter":[],"option_auto_color":[],"option_auto_size":[],"tags_gender_mhspyaq371nqa9w8y4ab3csl":[]},"numericFacets":{"price":["[0,100)","[100,200)","[200,300)","[300,400)","[400,500)","[500,2147483647)"]},"numericFacetFilters":{},"textFacetQuery":null,"geo":{}}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)