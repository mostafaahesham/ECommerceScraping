import requests
import json
import os
import time

itemDetailsURL = 'https://www.lcwaikiki.eg/en-US/EG/ajax/ProductGroup/ProductGroupPageData?xhrKeys=CountryCode,ProductGroup,ProductGender,xhrKeys&CountryCode=EG&ProductGroup={}&ProductGender={}&PageIndex={}'
main_url = "https://www.lcwaikiki.eg"

sections = {
    "Men": [1,1],
    "Women": [2,2],
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

pd_file = 'LC Waikiki/lcwaikiki_db.json'

if os.path.exists(pd_file):
    os.remove(pd_file)
else:
    print("Can not delete the file as it doesn't exists")

time.sleep(1)

lcwaikiki_stock = []

for section in sections:
    initial_response = requests.get(itemDetailsURL.format(sections[section][0],sections[section][1],1),headers=headers)
    page_count = initial_response.json()['CatalogList']['PageCount']
    item_count = initial_response.json()['CatalogList']['ItemCount']
    print("Get Initial Request Status Code", initial_response.status_code)
    print("{} Items, {} Pages Found in {} Section".format(item_count,page_count,section))
    for page in range(1,page_count+1):
        response = requests.get(itemDetailsURL.format(sections[section][0],sections[section][1],page),headers=headers)
        print(f'Get {section} Page {page} Status Code =', response.status_code)
        items = response.json()['CatalogList']['Items']
        for item in items:
            lcwaikiki_stock.append(
                {
                    'brand': "LC Waikiki",
                    'section': section,
                    # 'category': category,
                    'id': item['ModelId'],
                    'name': item['ProductDescription'],
                    'original price': item['OldPrice'],
                    'new price': item['Price'],
                    'discount': item['Discounted'],
                    'link': main_url + str(item['ModelUrl']).replace(u"\u2019", "'"),
                }
            )
        
with open(pd_file, 'w',encoding="UTF-8") as outfile:
    outfile.write(json.dumps(lcwaikiki_stock,indent=4))
