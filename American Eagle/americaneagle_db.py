import requests
import json
import os
import pandas as pd
from googletrans import Translator
import numpy as np

brand_name = "American Eagle"

main_url = "https://www.americaneagle.com.eg"
db_url = "https://sk1ql8dgia-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(16.9.0)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=SK1QL8DGIA&x-algolia-api-key=2f1a762808fec3bad0a5b67ee019a461"

db_file_name = "americaneagle_stock.json"
sample_file_name = "ae_sample.json"
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

size_aliases = {
    "XXS": "XXS",
    "XS":"صغير جداً",
    "S":"صغير",
    "M":"وسط",
    "L":"كبير",
    "XL":"كبير جداً",
    "XXL": "XXL",
    "XXXL": "XXXL"
}

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

translator = Translator()

for section in sections:
    for category in sections[section]:
        response = requests.post(db_url,json=sections[section][category])
        if response.status_code == 200:
            category_items = response.json()['results'][0]
            item_count = category_items['nbHits']
            print('Get {} Items from "{} {}" Section Status Code'.format(item_count,section,category), response.status_code)
            for item in category_items['hits']:
                sizes = []
                try:
                    item_id = item['objectID'][:-3].replace('-','')
                    
                    if int(item_id) not in ids:
                        ids.append(int(item_id))
                    else:
                        pass
                    
                    arabic_sizes = item['attr_size']['ar'][:-1] if "6 Short" in item['attr_size']['ar'] else item['attr_size']['ar'] # in stock sizes are in arabic
                    english_sizes = item['attr_size']['en'][:-1] if "6 Short" in item['attr_size']['en'] else item['attr_size']['en'] # available sizes are in english
                    
                    for size in english_sizes:
                        if size[0].isalpha():
                            sz = {
                                'name': size,
                                'availability': True if size_aliases[size] in arabic_sizes else False,
                            }
                        else:
                            sz = {
                                'name': size,
                                'availability': True if size in arabic_sizes else False
                            }
                            
                        sizes.append(sz)
                    
                    unmerged_stock.append(
                                {
                                    'item_brand': brand_name,
                                    'item_section': section,
                                    'item_category': category[:-2],
                                    'item_id': int(item_id),
                                    'item_name': item['title']['en'],
                                    'item_on_sale': True if (item['discount']['en'] != 0) else False,
                                    'item_old_price': item['original_price']['en'],
                                    'item_new_price': item['final_price']['en'],
                                    'item_discount': item['discount']['en'],
                                    'item_link': main_url + item['url']['en'],
                                    'color': translator.translate(item['attr_color']['ar'][0]).text.title(),
                                    'color_code':item['objectID'][-3:],
                                    'color_image': [image['url'] for image in item['media'] if '_f.' in image['url'] or '_of.' in image['url']][0],
                                    'images': [image['url'] for image in item['media']],
                                    'sizes': sizes                           
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

with open(db_file_path, "w", encoding='utf-8') as outfile:
    outfile.write(json.dumps(stock, indent=4,ensure_ascii = False,cls=NpEncoder))