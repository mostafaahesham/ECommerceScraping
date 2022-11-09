import os
import time
import json
import requests

main_url = "https://www.pullandbear.com/eg/en/"

itemIDsURL = 'https://www.pullandbear.com/itxrest/3/catalog/store/25009542/20309439/category/{}/product?languageId=-1&showProducts=false&appId=1'
itemDetailsURL = 'https://www.pullandbear.com/itxrest/3/catalog/store/25009542/20309439/productsArray?productIds={}&languageId=-1&categoryId={}&appId=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

itemIDsCategories = {
    'Men': {
        'Sweatshirts & Hoddies':'1030319522',
        'Trousers': '1030319526',
        'Jackets': '1030319521',
        'T-Shirts': '1030319523',
        'Jeans': '1030319527',
        'Shirts': '1030319524',
        'Knit': '1030319525',
        'Shorts': '1030319528',
        # 'Swimwear': '1030319530', # No Stock, Last Checked 2/10/2022
        'Shoes': '1030319531',
        'Accessories': '1030319536',
    },
    'Women': {
        'Trousers': '1030318047',
        'Sweatshirts & Hoddies': '1030314002',
        'T-Shirts': '1030313513',
        'Jackets': '1030313510',
        'Coats': '1030313509',
        'Knit': '1030314004',
        'Jeans': '1030318045',
        'Blouses & Shirts': '1030313514',
        'Dresses': '1030313511',
        'Skirts': '1030314005',
        'Tops & Bralettes': '1030318046',
        'Dungarees & Jumpsuits': '1030313512',
        'Shorts': '1030314006',
        # 'Swimwear': '1030319529', # No Stock, Last Checked 2/10/2022
        'Shoes': '1030318049',
        'Bags': '1030319516',
        'Accessories': '1030319505'
    }
}

# Parsed Data File
pd_file = 'Pull & Bear/pullandbear_db.json' 

# Delete file if it exists
if os.path.exists(pd_file):
    os.remove(pd_file)
else:
    print("Can not delete the file as it doesn't exists")

time.sleep(1)

pullandbear_stock = []

for section in itemIDsCategories.keys():
    for category in itemIDsCategories[section].keys():
        ids_response = requests.get(itemIDsURL.format(itemIDsCategories[section][category]),headers=headers)
        print('Get "{} {}" Items IDs Status Code'.format(section,category), ids_response.status_code)
        itemIDs = ''
        for id in ids_response.json()['productIds']:
            itemIDs = itemIDs + str(id) + ','
            
        response = requests.get(itemDetailsURL.format(itemIDs,itemIDsCategories[section][category]),headers=headers)
        print('Get {} Items from "{} {}" Status Code'.format(len(ids_response.json()['productIds']),section,category), response.status_code)
        if response.status_code == 200:
            category_items = response.json()
            try:
                for item in category_items['products']:
                    old_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['oldPrice']
                    new_price = item['bundleProductSummaries'][0]['detail']['colors'][0]['sizes'][0]['price']
                    
                    pullandbear_stock.append(
                            {
                                'brand': "Pull & Bear",
                                'section': section,
                                'category': category,
                                # sub category ??
                                'name': item['name'],
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
            print("No Items Could be fetched")

with open(pd_file, 'w') as f:
    f.write(json.dumps(pullandbear_stock))