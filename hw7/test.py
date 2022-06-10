from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
print(client.list_database_names())
# client.drop_database('DB_hw7')
print(client.list_database_names())
db = client['DB_hw7']
print(db.list_collection_names())
col = db['castoramaru']
control_list = []
for doc in col.find({}):
    print(doc['price_sale'])
    print(doc['price_true'])
    print(doc['currency'])