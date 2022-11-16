import os
import json
import requests
from math import ceil
import random

brand_name = "Bershka"

main_url = "https://www.bershka.com/eg/en/"
images_url = "https://static.bershka.net/4/photos2"
ids_url = "https://www.bershka.com/itxrest/3/catalog/store/45109542/40259544/category/{}/product?showProducts=false&languageId=-1"
db_url = "https://www.bershka.com/itxrest/3/catalog/store/45109542/40259544/productsArray?categoryId={}&productIds={}&languageId=-1"

links_file_name = "links.json"
db_file_name = "bershka_stock.json"
sample_file_name = 'bershka_sample.json'

main_path = os.path.dirname(os.path.realpath(__file__))

links_file_path = os.getcwd() + "\\" + links_file_name
db_file_path = main_path + "\\" + db_file_name
sample_file_path = main_path + "\\" + sample_file_name
    
availability_aliases = {
    "BACK_SOON":False,
    "COMING_SOON":False,
    "SOLD_OUT":False,
    "HIDDEN":False,
    "SHOW":True
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand_name] 
    
# save a raw sample for reference from a category that has more than 20 items   
for section in sections:
    for category in sections[section]:
        ids_response = requests.get(str(ids_url).format(sections[section][category]),headers=headers)
        print('Get "{} {}" Items IDs Status Code'.format(section,category), ids_response.status_code)
        itemIDs = ''
        for id in ids_response.json()['productIds']:
            itemIDs = itemIDs + str(id) + ','
            
        response = requests.get(db_url.format(format(sections[section][category]),itemIDs),headers=headers)
        print('Get {} Items from "{} {}" Status Code'.format(len(ids_response.json()['productIds']),section,category), response.status_code)
        if response.status_code == 200:
            category_items = response.json()
            if len(category_items['products']) > 20:
                with open(sample_file_path, "w") as outfile:
                    outfile.write(json.dumps(response.json(), indent=4))
                print("{} {} Sample Saved".format(section,category))
                break
            else:
                continue
    break

print("----------------------------------------------------------------------------")

stock = []
links = []

for section in sections:
    for category in sections[section]:
        ids_response = requests.get(ids_url.format(sections[section][category]),headers=headers)
        print('Get "{} - {}" Items IDs Status Code'.format(section,category[:-2]), ids_response.status_code)
        itemIDs = ''
        for id in ids_response.json()['productIds']:
            itemIDs = itemIDs + str(id) + ','
            
        response = requests.get(db_url.format(format(sections[section][category]),itemIDs),headers=headers)
        print('Get {} Items from "{} - {}" Status Code'.format(len(ids_response.json()['productIds']),section,category[:-2]), response.status_code)
        if response.status_code == 200:
            category_items = response.json()
            try:
                for item in category_items['products']:
                    try:
                        old_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['oldPrice']
                        new_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['price']
                        
                        choices = item['bundleProductSummaries'][0]['detail']['colors']
                        medias = item['bundleProductSummaries'][0]['detail']
                        
                        colors = {}
                        
                        for color in choices:
                            colors[str(color['id'])] = str(color['name'])
        
                        options = []
                        
                        for color in choices:
                            choice = {
                                "color": color['name'],
                                "color_code": color['id'],
                                "color_image":[],
                                "images":[],
                                "sizes":[]
                            }
                            
                            for size in color['sizes']:
                                choice['sizes'].append(
                                {
                                    "name": size['name'],
                                    "availability": availability_aliases[size['visibilityValue']]
                                }   
                                )

                            for media in medias['xmedia']:
                                for media_item in media['xmediaItems']:
                                    if media_item['set'] == 0:
                                        for m_item in media_item['medias']:
                                            if 'hash' not in m_item['extraInfo'].keys():
                                                pass
                                            else:
                                                if m_item["clazz"] == 1:
                                                    choice['images'].append(images_url + media['path'] + 
                                                                            '/' + 
                                                                            m_item['extraInfo']['hash'][0]['md5Hash'] + 
                                                                            '-' + 
                                                                            m_item['idMedia'] + '0.jpg')
                                                if m_item["clazz"] == 2:
                                                    choice['color_image'].append(images_url + media['path'] + 
                                                                            '/' + 
                                                                            m_item['extraInfo']['hash'][0]['md5Hash'] + 
                                                                            '-' + 
                                                                            m_item['idMedia'] + '0.jpg')
                                    else:
                                        pass                            
                                
                            options.append(choice)
                                
                        stock.append(
                                {
                                    'item_brand': brand_name,
                                    'item_section': section,
                                    'item_category': category[:-2],
                                    'item_id': item['id'],
                                    'item_name': item['name'],
                                    'item_on_sale': True if (old_price is not None) else False,
                                    'item_old_price': int(old_price[:-2]) if (old_price is not None) else int(new_price[:-2]),
                                    'item_new_price': int(new_price[:-2]),
                                    'item_discount': int(ceil(100*(1-(int(new_price[:-2]) / int(old_price[:-2]))))) if (old_price is not None) else 0,
                                    'item_link': main_url + item['productUrl'],
                                    'item_options': options                               
                                }
                        )
                        
                        links.append(item['productUrl'])
                    except Exception as e: print(e)
            except:
                print("Product not found")
        else:
            print("No Items Could be fetched")        
            
for item in stock:
    for option in item['item_options']:
        new_images = []
        for image in option['images']:
            if "/{}/".format(option['color_code']) in image:
                new_images.append(image) if image not in new_images else print("dup")
        option['images'] = new_images
        
        for color_image in option['color_image']:
            if "/{}/".format(option['color_code']) in color_image:
                option['color_image'] = color_image
        sizes = {}
        for size in option['sizes']:
            sizes[size['name']] = None

        size_options = []
        single_sizes_count = len(sizes.keys())
        dup_sizes_count = len(option['sizes'])
        step = ceil(dup_sizes_count/single_sizes_count)

        for size_name in sizes.keys():
            availability = False
            for i in range(step):
                availability |= option['sizes'][i]['availability']
            size_options.append(
                {
                    "name": size_name,
                    "availability": availability
                }
            )
            
        option['sizes'] = size_options
    try:
        item['default_color'] = item['item_options'][0]['color']
        item['default_size'] = item['item_options'][0]['sizes'][0]
        item['default_image'] = item['item_options'][0]['images'][0]
    except:
        print(item['item_id'])
    
                        
with open(db_file_path, 'w') as f:
    f.write(json.dumps(stock))