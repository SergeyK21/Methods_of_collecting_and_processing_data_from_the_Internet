from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
print(client.list_database_names())
# client.drop_database('vacancyDB')
# client.drop_database('booksDB')
print(client.list_database_names())
db = client['booksDB']
print(db.list_collection_names())
col = db['labirintru']
control_list = []
for doc in col.find({}):
    print(doc['price_real'], doc['price_sale'], doc['currency'])
#     print(doc['salary_min'], doc['salary_max'], doc['currency'])
    # if len(doc['salary']) == 8:
    #     pass
