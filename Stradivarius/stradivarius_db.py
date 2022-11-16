import requests
import json
import os
from math import ceil

brand_name = "Stradivarius"

main_url = "https://www.stradivarius.com/eg/en/"
images_url = "https://static.e-stradivarius.net/5/photos3"
db_url = "https://www.stradivarius.com/itxrest/3/catalog/store/55009592/50331101/category/{}/product?languageId=-1&showProducts=true&appId=1"

links_file_name = "links.json"
db_file_name = "stradivarius_stock.json"
sample_file_name = 'stradivarius_sample.json'

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

for section in sections:
    for category in sections[section]:
        response = requests.get(db_url.format(format(sections[section][category])),headers=headers)
        if response.status_code == 200:
            print('Get {} Items from "{} - {}" Status Code'.format(len(response.json()['productIds']),section,category[:-2]), response.status_code)
            if len(response.json()['productIds']) > 20:
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
        response = requests.get(db_url.format(format(sections[section][category])),headers=headers)
        if response.status_code == 200:
            print('Get {} Items from "{} - {}" Status Code'.format(len(response.json()['productIds']),section,category[:-2]), response.status_code)
            category_items = response.json()
            try:
                for item_id in category_items['productIds']:
                    item = category_items['products'][str(item_id)]
                    try:
                        old_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['oldPrice']
                        new_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['price']
                        
                        choices = item['bundleProductSummaries'][0]['detail']['colors']
                        medias = item['bundleProductSummaries'][0]['detail']
                        
                        colors = {}
                        
                        for color in choices:
                            colors[str(color['id'])] = str(color['name'])
        
                        options = []
                        for color,media in zip(choices,medias['xmedia']):
                            if media['colorCode'] in colors.keys():
                                choice = {
                                    "color": colors[media['colorCode']],
                                    "color_code": str(media['colorCode']),
                                    "color_image":[],
                                    "main_image":None,
                                    "images":[],
                                    "sizes": {},
                                    
                                }

                            for media in medias['xmedia']:
                                for media_item in media['xmediaItems']:
                                    if media_item['set'] == 0:
                                        for m_item in media_item['medias']:
                                            choice['images'].append(images_url + media['path'] + 
                                                                    '/' + 
                                                                    m_item['idMedia'] + '2.jpg') if m_item['clazz'] != 10 and m_item['clazz'] != 3 else print("")
                                        break
                                    else:
                                        pass
                                
                            for size in color['sizes']:
                                if size['name'] not in choice['sizes'].keys():
                                    choice["sizes"][size['name']] = availability_aliases[size['visibilityValue']]
                                else:
                                    choice["sizes"][size['name']] |= availability_aliases[size['visibilityValue']]
                                
                            options.append(choice)
                                
                        stock.append(
                                {
                                    'item_brand': brand_name,
                                    'item_section': section,
                                    'item_category': category[:-2],
                                    'item_id': item['id'],
                                    'item_name': item['bundleProductSummaries'][0]['name'],
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
            except Exception as e: print(e)
        else:
            print("No Items Could be fetched")
            
for item in stock:
    for option in item['item_options']:
        new_images = []
        for image in option['images']:
            if "/{}/".format(option['color_code']) in image:
                new_images.append(image) if image not in new_images else print("dup")
        option['images'] = new_images
        option['main_image'] = new_images[0]
        
        for color_image in option['color_image']:
            if "/{}/".format(option['color_code']) in color_image:
                option['color_image'] = color_image
    
                        
with open(db_file_path, 'w') as f:
    f.write(json.dumps(stock))