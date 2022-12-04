import requests
import json
import os
import time
import math
import numpy as np
import pandas as pd


brand_name = "Defacto"

main_url = "https://www.defacto.com/en-eg/"
images_url = "https://dfcdn.defacto.com.tr/7/"

db_file_name = "defacto_stock.json"
sample_file_name = "defacto_sample.json"
links_file_name = "links.json"

main_path = os.path.dirname(os.path.realpath(__file__))

links_file_path = os.getcwd() + "/" + links_file_name
db_file_path = main_path + "/" + db_file_name
sample_file_path = main_path + "/" + sample_file_name

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand_name] 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

for section in sections:
    for category in sections[section]:
        initial_response = requests.get(sections[section][category].format(1),headers=headers)
        if initial_response.status_code == 200:
            print('Get "{} {}" Initial Request Status Code'.format(section,category), initial_response.status_code)
            item_count = initial_response.json()['Data']['SearchResponse']['Count']
            page_count = math.ceil(item_count/60)
            print('{} Items, {} Pages Found in "{} {}" Section'.format(item_count,page_count,section,category))
            if item_count > 30:
                response = requests.get(sections[section][category].format(1),headers=headers)
                if response.status_code == 200:
                    items = response.json()['Data']['SearchResponse']['Documents']
                    with open(sample_file_path, "w",encoding="utf-8") as outfile:
                        outfile.write(json.dumps(response.json(), indent=4,ensure_ascii = False))
                    print("{} {} Sample Saved".format(section,category))
                    break
                else:
                    print("{} {} bad request".format(section,category))
            else:
                continue
        else:
            print("{} {} bad request".format(section,category))
    break
                
print("-------------------------------------------")

unmerged_stock = []
ids = []

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

for section in sections:
    for category in sections[section]:
        initial_response = requests.get(sections[section][category].format(1),headers=headers)
        if initial_response.status_code == 200:
            print('Get "{} {}" Initial Request Status Code'.format(section,category), initial_response.status_code)
            item_count = initial_response.json()['Data']['SearchResponse']['Count']
            page_count = math.ceil(item_count/60)
            print('{} Items, {} Pages Found in "{} {}" Section'.format(item_count,page_count,section,category))
            for page in range(1,page_count+1):
                response = requests.get(sections[section][category].format(page),headers=headers)
                if response.status_code == 200:
                    size_aliases = {}
                    size_indicies = response.json()['Data']['SearchResponse']['Facets'][2]['SearchFacetItems']
                    for size_index in size_indicies:
                        size_aliases[str(size_index['Index'])] = size_index['Term']
                    items = response.json()['Data']['SearchResponse']['Documents']
                    print('Get "{} {}" Page {} Status Code = '.format(section,category,page), response.status_code)
                    for item in items:
                        try:
                            item_id = item['ProductMainCode']
                            
                            if int(item_id[1:5]) not in ids:
                                ids.append(int(item_id[1:5]))
                            else:
                                pass
                            
                            unmerged_stock.append(
                                {
                                    'item_brand': "Defacto",
                                    'item_section': section,
                                    'item_category': category,
                                    'item_id': int(item_id[1:5]),
                                    'item_name': item['ProductName'],
                                    'item_on_sale': True if item['ProductPriceInclTax'] != item['ProductVariantDiscountedPriceInclTax'] else False,
                                    'item_old_price': item['ProductPriceInclTax'],
                                    'item_new_price': item['ProductVariantDiscountedPriceInclTax'],
                                    'item_discount': int(math.ceil(item["DiscountRate"])),
                                    'item_link': main_url + item['ProductSeoName'] + "-" + str(item["ProductVariantIndex"]),
                                    'color': item['ColorGtmName'].replace(" ",''),
                                    'color_code': item_id[7:],
                                    'color_image': [images_url + img['ProductPicturePath'] for img in item['ProductPictures'] if img['ProductPictureIsDefault'] == True][0],
                                    'images': [images_url + img['ProductPicturePath'] for img in item['ProductPictures']],
                                    'sizes' : [{'name': size_aliases[str(size['SizeIndex'])],'availability': True} for size in item['Sizes']] 
                                }
                            )
                        except Exception as e:print(e)
                else:
                    print("{} Bad Request".format(section))
            
print('--------------------Merging Data---------------------')
            
df = pd.DataFrame(unmerged_stock)
stock = []

for id in ids:
    item = df.loc[df['item_id'] == id]
    options = item[['color','color_code','color_image','images','sizes']]

    item_options = []

    for i in range(len(options)):
        option = {
                "color": options.iloc[i]['color'],
                "color_code": options.iloc[i]['color_code'],
                "color_image": options.iloc[i]['color_image'],
                "images": options.iloc[i]['images'],
                "sizes": options.iloc[i]['sizes']
            }
        item_options.append(option)
    try:        
        stock.append(
            {
                'item_brand': item.iloc[0]['item_brand'],
                'item_section': item.iloc[0]['item_section'],
                'item_category': item.iloc[0]['item_category'],
                'item_id': item.iloc[0]['item_id'],
                'item_name': item.iloc[0]['item_name'],
                'item_on_sale': bool(item.iloc[0]['item_on_sale']),
                'item_old_price': item.iloc[0]['item_old_price'],
                'item_new_price': item.iloc[0]['item_new_price'],
                'item_discount': item.iloc[0]['item_discount'],
                'item_link': item.iloc[0]['item_link'],
                'item_options': item_options
            }
        )
    except Exception as e:print(e)
    
for item in stock:
    try:
        item['default_option'] = {
            "default_color": item['item_options'][0]['color'],
            "default_color_code": item['item_options'][0]['color_code'],
            "default_size": item['item_options'][0]['sizes'][0],
            "default_image": item['item_options'][0]['images'][0],           
        }
    except Exception as e:print(e,item['item_id'])

with open(db_file_path, "w", encoding='utf-8') as outfile:
    outfile.write(json.dumps(stock, indent=4,ensure_ascii = False,cls=NpEncoder))