import requests
import json
import os
import pandas as pd
import numpy as np
import math

brand_name = "Concrete"

main_url = "https://concrete.store/en/product/"
db_url = "https://concrete.store/en/List/search"
payload = {
    "CategoryID": None,
    "CustomListID": "",
    "PageIndex": 1,
    "RowCount": 3000,
    "SortProp": "newarrivals",
    "ShowCategoryTree": True,
    "ColorsIDs": [],
    "SizesIDs": [],
    "BrandsIDs": [],
    "CategoriesIDs": [None],
    "ColorGroupIDs": [],
    "FeatureValues": [],
}

db_file_name = "concrete_stock.json"
sample_file_name = "concrete_sample.json"
links_file_name = "links.json"

main_path = os.path.dirname(os.path.realpath(__file__))

links_file_path = os.getcwd() + "/" + links_file_name
db_file_path = main_path + "/" + db_file_name
sample_file_path = main_path + "/" + sample_file_name

with open(links_file_path, encoding="UTF-8") as sections_file:
    sections = json.load(sections_file)[brand_name]

for section in sections:
    for category in sections[section]:
        
        payload['CategoryID'] = sections[section][category]
        payload['CategoriesIDs'][0] = sections[section][category]
        
        response = requests.post(db_url, json=payload)
        if response.status_code == 200:
            item_count = response.json()["TotalCount"]
            print(
                'Get {} Items from "{} {}" Section Status Code'.format(
                    item_count, section, category
                ),
                response.status_code,
            )
            if item_count > 20:
                with open(sample_file_path, "w", encoding="utf-8") as outfile:
                    outfile.write(
                        json.dumps(response.json(), indent=4, ensure_ascii=False)
                    )
                print("{} {} Sample Saved".format(section, category))
                break
            else:
                continue
        else:
            print("{} {} bad request".format(section, category))
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
        
        payload['CategoryID'] = sections[section][category]
        payload['CategoriesIDs'][0] = sections[section][category]
        
        response = requests.post(db_url, json=payload)
        
        if response.status_code == 200:
            print('Get "{} {}" Status Code'.format(section,category), response.status_code)
            item_count = response.json()["TotalCount"]
            print('{} Items Found in "{} {}" Section'.format(item_count,section,category))
            category_items = response.json()['Result']
            for item in category_items:
                try:
                    id = item['Code'].split('-')[:4]
                    dummy_id = ''.join(id)

                    if dummy_id not in ids:
                        ids.append(dummy_id)
                    else:
                        pass
                    
                    unmerged_stock.append(
                                    {
                                        'item_brand': brand_name,
                                        'item_section': section,
                                        'item_category': category[:-2],
                                        'item_id': item['ID'],
                                        'item_name': item['Title'].title(),
                                        'item_on_sale': False if item['FinalPrice'] == item['Price'] else True,
                                        'item_old_price': int(math.ceil(item['Price'])),
                                        'item_new_price': int(math.ceil(item['FinalPrice'])),
                                        'item_discount': int(math.ceil(100*(1-(int(item['FinalPrice']) / int(item['Price']))))),
                                        'item_link': main_url + item['SEOTitle'],
                                        'dummy_id': dummy_id,
                                        'color': item['Color'].title(),
                                        'color_code': str(item['ColorID']),
                                        'color_image': item['ImageURL'],
                                        'images': [item['ImageURL'],item['SecondImageURL']],
                                        'sizes': [{'name': size['Name'], 'availability': True} for size in item['Sizes']]                           
                                    }
                            )
                except Exception as e:print(e)
        else:
            print("{} {} Bad Request".format(section,category))
            
print('--------------------Merging Data---------------------')

df = pd.DataFrame(unmerged_stock)
stock = []

for id in ids:
    item = df.loc[df['dummy_id'] == id]
    options = item[['color','color_code','color_image','images','sizes']]

    item_options = []
    dup_options = []

    for i in range(len(options)):
        option = {
                "color": options.iloc[i]['color'],
                "color_code": options.iloc[i]['color_code'],
                "color_image": options.iloc[i]['color_image'],
                "images": options.iloc[i]['images'],
                "sizes": options.iloc[i]['sizes']
            }
        if option not in dup_options:
            item_options.append(option)
            dup_options.append(option)
        else:
            print('dup_option')
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