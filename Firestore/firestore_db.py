import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Use a service account.
cred = credentials.Certificate('Firestore/serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

items_db = firestore.client()

file  = open('Stradivarius/stradivarius_stock.json')

item_stock = json.load(file)

def items_update():
    for item in item_stock:
        try:
            items_db.collection('itemStock').document(str(item['item_id'])).set({
                            "brand":item["item_brand"],
                            "section":item['item_section'],
                            "category":item['item_category'],
                            "id": item['item_id'],
                            "name":item["item_name"],
                            "sale": item['item_on_sale'],
                            "old_price":item["item_old_price"],
                            "new_price":item["item_new_price"],
                            "discount":item["item_discount"],
                            "link":item["item_link"],
                            "options":item['item_options'],
                            "default_color": item['default_color'],
                            "default_size": item['default_size'],
                            "default_image": item['default_image'],
                            })
            print("updating : {}".format(item['item_id']))
        except Exception as e:print(e)

items_update()