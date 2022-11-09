import requests
import json
import os

brand_name = "H&M"
 
main_url = "https://eg.hm.com"
db_url = "https://hgr051i5xn-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react%20(16.9.0)%3B%20react-instantsearch%20(5.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=HGR051I5XN&x-algolia-api-key=a2fdc9d456e5e714d8b654dfe1d8aed8"

db_file_name = "h&m_stock.json"
sample_file_name = "h&m_sample.json"
links_file_name = "links.json"

links_file_path = os.getcwd() + "\\" + links_file_name
main_path = os.path.dirname(os.path.realpath(__file__))
db_file_path = main_path + "\\" + db_file_name
sample_file_path = main_path + "\\" + sample_file_name

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand_name] 

for section in sections:
    for category in sections[section]:
        response = requests.post(db_url,json=sections[section][category])
        if response.status_code == 200:
            sample = response.json()['results'][0]
            item_count = sample['nbHits']
            if item_count > 20:
                with open(sample_file_path, "w") as outfile:
                    outfile.write(json.dumps(response.json(), indent=4))
                print("{} {} Sample Saved".format(section,category))
                print("-------------------------------------------")
                break
            else:
                continue
        else:
            print("{} {} bad request".format(section,category))
    break

hm_stock = []

for section in sections:
    for category in sections[section]:
        response = requests.post(db_url,json=sections[section][category])
        if response.status_code == 200:
            category_items = response.json()['results'][0]
            item_count = category_items['nbHits']
            print('Get {} Items from "{} {}" Section Status Code'.format(item_count,section,category), response.status_code)
            for item in category_items['hits']:
                hm_stock.append(
                    {
                        'item_brand': brand_name,
                        'item_section': section,
                        'item_category': category[:-2],
                        'item_id': item['nid'],
                        'item_name': str(item['title']['en']),
                        'item_original_price': item['original_price']['en'],
                        'item_new_price': item['final_price']['en'],
                        'item_discount': item['discount']['en'],
                        'item_link': main_url + item['url']['en'],
                        'item_sizes': item['attr_size']['en'] if "6 Short" not in item['attr_size']['en'] else item['attr_size']['en'][:-1],
                        'item_colors': item['attr_color']['en'] if len(item['attr_color']['en']) == 1 else None,
                        'item_images': [img['url'] for img in item['media']],
                        'item_availability': item['in_stock']['en']
                    }
                )
        else:
            print("{} {} Bad Request".format(section,category))
 
with open(db_file_path, "w") as outfile:
    outfile.write(json.dumps(hm_stock, indent=4))