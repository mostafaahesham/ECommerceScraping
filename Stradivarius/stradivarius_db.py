import requests
import json
import os
import time

main_url = "https://www.stradivarius.com/eg/en/"
itemDetailsURL = 'https://www.stradivarius.com/itxrest/2/catalog/store/55009592/50331101/category/{}/product?languageId=-1&appId=1'

itemIDsCategories = {
    'Women': {
        'Shirts & Blouses': '1718502',
        'Sweatshirts': '1718524',
        'Dresses': '1020035501',
        'T-Shirts': '1718528',
        'Tops & Bodysuits': '1020297562',
        'Cargo': '1020433956',
        'Jeans': '1718557',
        'Trousers': '1718516',
        'Shorts': '1020377546',
        'Skirts': '1718525',
        'Jackets': '1020192003',
        'Blazers': '1695505',
        'Waistcoats': '1020437417',
        'Knit': '1718564',
        'Shoes': '1020178528',
        'Accessories': '1020303541'
    }
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

pd_file = 'Stradivarius/stradivarius_db.json'

if os.path.exists(pd_file):
    os.remove(pd_file)
else:
    print("Can not delete the file as it doesn't exists")

time.sleep(1)

stradivarius_stock = []

for section in itemIDsCategories.keys():
    for category in itemIDsCategories[section].keys():
        response = requests.get(itemDetailsURL.format(itemIDsCategories[section][category]),headers=headers)
        if response.status_code == 200:
            print('Get "{} {}" Items Status Code'.format(section,category), response.status_code)
            category_items = response.json()
            try:
                for item in category_items['products']:
                    old_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['oldPrice']
                    new_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['price']
                    
                    stradivarius_stock.append(
                            {
                                'brand': "Stradivarius",
                                'section': section,
                                'category': category,
                                'id': item['id'],
                                'name': item['bundleProductSummaries'][0]['nameEn'],
                                'original price': old_price[:-2] if (old_price is not None) else new_price[:-2],
                                'new price': new_price[:-2],
                                'link': main_url + item['productUrl'],
                                # Availability ?
                                # images, sizes & colors should be list ?
                                
                            }
                    )
            except:
                print("Product not found")
        else:
            print("{} {} Bad Request".format(section,category))
        
with open(pd_file,'w',encoding="UTF-8") as outfile:
    outfile.write(json.dumps(stradivarius_stock,indent=4))