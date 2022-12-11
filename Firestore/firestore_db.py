import json
import os
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class MerchantDB:
    def __init__(_mdb, cn, bn, sak):
        _mdb.main_path = os.path.dirname(os.path.realpath(__file__))
        
        _mdb.collection_name = cn
        _mdb.brand_name = bn
        
        _mdb.cred = credentials.Certificate(_mdb.main_path + "/" + sak)
        _mdb.app = firebase_admin.initialize_app(_mdb.cred)
        _mdb.db = firestore.client()
        _mdb.db_file = None
        _mdb.collection_ref = _mdb.db.collection(cn)

    def load_db_file(_ldbf,db_file_path):
        _ldbf.db_file  = open(db_file_path)
        _ldbf.item_stock = json.load(_ldbf.db_file)

    def items_count(_ic):
        
        return len(_ic.collection_ref.get())

    def items_delete(_id,all,brand):
        if all == True:
            for doc in _id.collection_ref.stream():
                _id.collection_ref.document(doc.id).delete()
                
        else:
            if brand is not None:
                for doc in _id.collection_ref.where('brand', '==', brand).stream():
                    _id.collection_ref.document(doc.id).delete()
            else:
                print("MerchantDB::items_delete -> Error! No brand was chosen")
            
    def random_items(_ri):
        for i in range(20):
            y = random.randrange(len(_ri.item_stock))
            try:
                _ri.collection_ref.document(str(_ri.item_stock[y]['item_id'])).set({
                                "brand":_ri.item_stock[y]["item_brand"],
                                "section":_ri.item_stock[y]['item_section'],
                                "category":_ri.item_stock[y]['item_category'],
                                "id": _ri.item_stock[y]['item_id'],
                                "name":_ri.item_stock[y]["item_name"],
                                "sale": _ri.item_stock[y]['item_on_sale'],
                                "old_price":_ri.item_stock[y]["item_old_price"],
                                "new_price":_ri.item_stock[y]["item_new_price"],
                                "discount":_ri.item_stock[y]["item_discount"],
                                "link":_ri.item_stock[y]["item_link"],
                                "options":_ri.item_stock[y]['item_options'],
                                "default_option": _ri.item_stock[y]['default_option'],
                                })
                print("updating : {} - {} - {}".format(str(_ri.item_stock[y]['item_id']),_ri.item_stock[y]['item_brand'],_ri.item_stock[y]['item_name']))
            except Exception as e:print(e)
            
    def items_update(_iu):
        for item in _iu.item_stock:
            try:
                _iu.db.collection(_iu.collection_name).document(str(item['item_id'])).set({
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
                                "default_option": item['default_option'],
                                })
                print("updating : {} - {} - {}".format(str(item['item_id']),item['item_brand'],item['item_name']))
            except Exception as e:print(e)
            
brand_name = "Concrete"
collection_name = "itemStock"

merchant_db = MerchantDB(collection_name,brand_name,"serviceAccountKey.json")
merchant_db.load_db_file("{}/{}_stock.json".format(merchant_db.brand_name,merchant_db.brand_name.lower().replace(' ','')))

print(merchant_db.items_count())
# merchant_db.items_update()
# merchant_db.items_delete(False,brand_name)
# merchant_db.random_items()