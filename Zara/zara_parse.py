import pandas as pd
import json

from sqlalchemy import false, true

df = pd.read_json('Zara\zara_men_content.json')
brand = "Zara"
img_header1 = "https://static.zara.net/photos//"
img_header2 = "/"
img_footer = ".jpg?ts="
products = []
_availability = False
url_header = "https://www.zara.com/eg/en/"
url_mid = "-p"
url_footer = ".html"


for page in df['productGroups']:
    for item in page:
        for elem in item['elements']:
            try:
                if('header' in elem.keys()):
                    section = elem["header"].split("For")[0].strip()
                if('commercialComponents' in elem.keys()):
                    for names in elem['commercialComponents']:
                        if(names['name'] != ''):
                                pics = []
                                for image in names['xmedia']:
                                    pics.append(img_header1 + image['path'] + img_header2 + image['name'] + img_footer + image['timestamp'])
                                if('oldPrice' in names.keys()):
                                    oldPrice = names['oldPrice']
                                else:
                                    oldPrice = 0
                                if('displayDiscountPercentage' in names.keys()):
                                    discountPercentage = names['displayDiscountPercentage']
                                else: 
                                    discountPercentage = 0
                                
                                if names['availability'] == "in_stock":
                                    _availability = True
                                
                                item_url = url_header + names["seo"]["keyword"] + url_mid + names["seo"]["seoProductId"] + url_footer
                                    
                                product = {
                                    "item_brand" : brand,
                                    "item_section" : names['sectionName'],
                                    "item_category" : section,
                                    "item_id" : names["seo"]["discernProductId"],
                                    "item_name" : names['name'],
                                    "item_new_price" : names['price'],
                                    "item_old_price" : oldPrice,
                                    "item_discount" : discountPercentage,
                                    "item_link" : item_url,
                                    "item_options": [
                                        {
                                            "color" : names["detail"]["colors"][0]["name"],
                                            "color_code" : names["detail"]["colors"][0]["id"],
                                            # "color_image" : 
                                            "images" : pics,
                                            "sizes": [
                                                        {
                                                            "name" : None,
                                                            "availability":  _availability
                                                        }
                                                     ]
                                        }
                                        ]
                                   
                                    

                                }
                                products.append(product)
                                break
            except:
                print(names["name"])
              

# df = pd.read_json('zara_women_content.json')

# for page in df['productGroups']:
#     for item in page:
#         for elem in item['elements']:
#             try:
#                 if('commercialComponents' in elem.keys()):
#                     for names in elem['commercialComponents']:
#                         if(names['name'] != ''):
#                                 pics = []
#                                 header1 = "https://static.zara.net/photos//"
#                                 header2 = "/w/293/"
#                                 footer = ".jpg?ts="
#                                 for image in names['xmedia']:
#                                     pics.append(header1 + image['path'] + header2 + image['name'] + footer + image['timestamp'])
#                                 if('description' in names.keys()):
#                                     description = names['description']
#                                 elif('description' in elem.keys()):
#                                     description = elem['description']
#                                 else:
#                                     description = ''
                                    
#                                 product = {
#                                     "name" : names['name'],
#                                     "description" : description,
#                                     "price" : names['price'],
#                                     "section" : names['sectionName'],
#                                     "availability" : names['availability'],
#                                     "images" : pics

#                                 }
#                                 products.append(product)
#             except:
#                 print(names)
              


json_object = json.dumps(products,indent=4)
with open('zara_sample.json','w') as out:
   out.write(json_object)
# print(products)