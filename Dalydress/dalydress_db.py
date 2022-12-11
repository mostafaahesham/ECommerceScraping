import requests
import json
import os
import math
import numpy as np
import pandas as pd

brand_name = "Dalydress"

main_url = "https://dalydress.com/products/"
db_url = "https://xytpiqsykygz2k2wtthklmcu-fast.searchtap.net/v2"

db_file_name = "dalydress_stock.json"
sample_file_name = "dalydress_sample.json"
links_file_name = "links.json"

main_path = os.path.dirname(os.path.realpath(__file__))

links_file_path = os.getcwd() + "/" + links_file_name
db_file_path = main_path + "/" + db_file_name
sample_file_path = main_path + "/" + sample_file_name

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand_name] 
    
headers = {"authorization": "Bearer 2DYJG7BEJD5BCAW1Q9Z3NLHD"}
    
for section in sections:
    for category in sections[section]:
        response = requests.post(db_url,headers=headers,json = sections[section][category])
        if response.status_code == 200:
            print('Get "{} {}" Initial Request Status Code'.format(section,category), response.status_code)
            item_count = response.json()['totalHits']
            print('{} Items Found in "{} {}" Section'.format(item_count,section,category))
            if item_count > 30:
                    with open(sample_file_path, "w",encoding="utf-8") as outfile:
                        outfile.write(json.dumps(response.json(), indent=4,ensure_ascii = False))
                    print("{} {} Sample Saved".format(section,category))
                    break

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
        response = requests.post(db_url,headers=headers,json = sections[section][category])
        if response.status_code == 200:
            print('Get "{} {}" Status Code'.format(section,category), response.status_code)
            item_count = response.json()['totalHits']
            print('{} Items Found in "{} {}" Section'.format(item_count,section,category))
            category_items = response.json()['results']
            for item in category_items:
                try:
                    id = item['handle'].split('-')[:-1]
                    color_code = item['handle'].split('-')[-1]
                    
                    item_id = int(''.join(id))

                    if item_id not in ids:
                        ids.append(item_id)
                    else:
                        pass
                    
                    unmerged_stock.append(
                                    {
                                        'item_brand': brand_name,
                                        'item_section': section,
                                        'item_category': category[:-2],
                                        'item_id': item_id,
                                        'item_name': item['title'],
                                        'item_on_sale': False if item['discount'] == 0 else True,
                                        'item_old_price': int(math.floor(item['compare_at_price'])) if item['compare_at_price'] != 0 else int(math.floor(item['price'])),
                                        'item_new_price': int(math.floor(item['price'])),
                                        'item_discount': int(math.floor(item['discount'])),
                                        'item_link': main_url + item['handle'],
                                        'color': item['option_auto_color'][0].title(),
                                        'color_code': color_code,
                                        'color_image': item['image']['src'],
                                        'images': [img['src'] for img in item['images']],
                                        'sizes': [{'name': size.upper(), 'availability': True} for size in item['option_auto_size']]                           
                                    }
                            )
                except Exception as e:print(e)
        else:
            print("{} {} Bad Request".format(section,category))
            
print('--------------------Merging Data---------------------')
            
df = pd.DataFrame(unmerged_stock)
stock = []

for id in ids:
    item = df.loc[df['item_id'] == id]
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