import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Use a service account.
cred = credentials.Certificate('serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

file  = open('Bershka/bershka_stock.json')

item_stock = json.load(file)

def items_update():
    # for item in item_stock:
        # items_db.collection('itemStock').document(str(item['item_id'])).set({
        #                 "brand":item["item_brand"],
        #                 "section":item['item_section'],
        #                 "category":item['item_category'],
        #                 "id": item['item_id'],
        #                 "name":item["item_name"],
        #                 "sale": item['item_on_sale'],
        #                 "old_price":item["item_old_price"],
        #                 "new_price":item["item_new_price"],
        #                 "discount":item["item_discount"],
        #                 "link":item["item_link"],
        #                 "options":item['item_options'],
        #                 "default_image": item['default_image'],
        #                 "default_color": item['default_color'],
        #                 "default_size": item['default_size']
        #                 })
    db.collection('itemStock').document("dfg").set({"4":"5"})
    print(5)

items_update()