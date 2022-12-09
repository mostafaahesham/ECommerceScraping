import json
import os
import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

main_path = os.path.dirname(os.path.realpath(__file__))

sak = "serviceAccountKey.json"
cred = credentials.Certificate(main_path + "/" + sak)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

db_file  = open('Dalydress/dalydress_stock.json')
item_stock = json.load(db_file)

def random_data():
    for i in range(50):
        y = random.randrange(len(item_stock))
        try:
            db.collection('itemStock').document(str(item_stock[y]['item_id'])).set({
                            "brand":item_stock[y]["item_brand"],
                            "section":item_stock[y]['item_section'],
                            "category":item_stock[y]['item_category'],
                            "id": item_stock[y]['item_id'],
                            "name":item_stock[y]["item_name"],
                            "sale": item_stock[y]['item_on_sale'],
                            "old_price":item_stock[y]["item_old_price"],
                            "new_price":item_stock[y]["item_new_price"],
                            "discount":item_stock[y]["item_discount"],
                            "link":item_stock[y]["item_link"],
                            "options":item_stock[y]['item_options'],
                            "default_option": item_stock[y]['default_option'],
                            })
            print("updating : {} - {} - {}".format(str(item_stock[y]['item_id']),item_stock[y]['item_brand'],item_stock[y]['item_name']))
        except Exception as e:print(e)
        
random_data()