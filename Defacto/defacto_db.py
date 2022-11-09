import requests
import json
import os
import time
import math

main_url = "https://www.defacto.com/en-eg/"

categories = {
    'Men':
        {
          'T-Shirts': ["https://www.defacto.com/en-eg/Catalog/PartialIndexScrollResult?page={}&SortOrder=0&pageSize=60&q=&fx_c1=1610&fx_c2=1616&fx_c3=1630"],
          'Shirts': ["https://www.defacto.com/en-eg/Catalog/PartialIndexScrollResult?page=2&SortOrder=0&pageSize=60&q=&fx_c1=1610&fx_c2=1616&fx_c3=1629"],
          'Knitwear & Sweatshirts': [
              "https://www.defacto.com/en-eg/Catalog/PartialIndexScrollResult?page=2&SortOrder=0&pageSize=60&q=&fx_c1=1610&fx_c2=1616&fx_c3=1631",
              "https://www.defacto.com/en-eg/Catalog/PartialIndexScrollResult?page=2&SortOrder=0&pageSize=60&q=&fx_c1=1610&fx_c2=1616&fx_c3=1645",
              ],
          'Jackets & Coats': [
              "https://www.defacto.com/en-eg/Catalog/PartialIndexScrollResult?page=2&SortOrder=0&pageSize=60&q=&fx_c1=1610&fx_c2=1616&fx_c3=1665" # Cardigans URL missing,
              ""
              ],
        },
    'Women': '1608',
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}

pd_file = 'Defacto/defacto_db.json'

if os.path.exists(pd_file):
    os.remove(pd_file)
else:
    print("Can not delete the file as it doesn't exist")

time.sleep(1)

defacto_stock = []

for section in sections:
    initial_response = requests.get(itemDetailsURL.format(1,sections[section]),headers=headers)
    print('Get "{}" Initial Request Status Code'.format(section), initial_response.status_code)
    items_count = initial_response.json()['Data']['SearchResponse']['Count']
    page_count = math.ceil(items_count/60)
    print('{} Items, {} Pages Found in "{}" Section'.format(items_count,page_count,section))
    for page in range(1,page_count+1):
        response = requests.get(itemDetailsURL.format(page,sections[section],page),headers=headers)
        if response.status_code == 200:
            items = response.json()['Data']['SearchResponse']['Documents']
            print(f'Get {section} Page {page} Status Code =', response.status_code)
            for item in items:
                defacto_stock.append(
                    {
                        'brand': "Defacto",
                        'section': section,
                        # 'category': category,
                        'id': item['ProductId'],
                        'name': item['ProductName'],
                        'original price': item['ProductPriceInclTax'],
                        'new price': item['ProductVariantDiscountedPriceInclTax'],
                        'discount': item["DiscountRate"],
                        'link': main_url + item['ProductSeoName'] + "-" + str(item["ProductVariantIndex"]),
                    }
                )
        else:
            print("{} Bad Request".format(section))
            
with open(pd_file, 'w') as outfile:
    outfile.write(json.dumps(defacto_stock,indent=4))