import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate(r'Firestore/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

file  = open('Bershka/bershka_stock.json')

item_stock = json.load(file)

items_db = firestore.client()

def items_update():
    for item in item_stock:
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
                        "options":item['item_options']
                        })
        
items_update()