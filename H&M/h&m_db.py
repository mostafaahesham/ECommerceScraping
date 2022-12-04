import requests
import json
import os
import pandas as pd
import numpy as np

brand_name = "H&M"
 
main_url = "https://eg.hm.com"
db_url = "https://hgr051i5xn-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(16.9.0)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=HGR051I5XN&x-algolia-api-key=a2fdc9d456e5e714d8b654dfe1d8aed8"

db_file_name = "h&m_stock.json"
sample_file_name = "h&m_sample.json"
links_file_name = "links.json"

main_path = os.path.dirname(os.path.realpath(__file__))
links_file_path = os.getcwd() + "/" + links_file_name
db_file_path = main_path + "/" + db_file_name
sample_file_path = main_path + "/" + sample_file_name

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand_name] 

for section in sections:
    for category in sections[section]:
        response = requests.post(db_url,json=sections[section][category])
        if response.status_code == 200:
            sample = response.json()['results'][0]
            item_count = sample['nbHits']
            print('Get {} Items from "{} {}" Section Status Code'.format(item_count,section,category), response.status_code)
            if item_count > 20:
                with open(sample_file_path, "w") as outfile:
                    outfile.write(json.dumps(response.json(), indent=4))
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
        response = requests.post(db_url,json=sections[section][category])
        if response.status_code == 200:
            category_items = response.json()['results'][0]
            item_count = category_items['nbHits']
            print('Get {} Items from "{} {}" Section Status Code'.format(item_count,section,category), response.status_code)
            for item in category_items['hits']:
                # sizes = []
                try:
                    item_id = item['sku']
                    
                    if int(item_id[:-3]) not in ids:
                        ids.append(int(item_id[:-3]))
                    else:
                        pass
                    
                    unmerged_stock.append(
                        {
                            'item_brand': brand_name,
                            'item_section': section,
                            'item_category': category[:-2],
                            'item_id': int(item_id[:-3]),
                            'item_name': str(item['title']['en']),
                            'item_on_sale': True if (item['discount']['en'] != 0) else False,
                            'item_old_price': item['original_price']['en'],
                            'item_new_price': item['final_price']['en'],
                            'item_discount': item['discount']['en'],
                            'item_link': main_url + item['url']['en'],
                            'color': item['attr_color_label']['en'][0],
                            'color_code': item_id[-3:],
                            'color_image': [image['url'] for image in item['media'] if image['image_type'] == "DescriptiveStillLife"][0],
                            'images': [img['url'] for img in item['media']],
                            'sizes': [{'name': size,'availability': True} for size in item['attr_size']['en']]
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