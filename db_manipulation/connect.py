from pymongo import MongoClient
import os

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.hubspot
    print("Connect to database")
except Exception as e:
    print(e)

def create_collections():
        try:
        db.drop_collection('services_provide')
        #db.services_provide.drop_index()
        db.create_collection('services_provide')
        db.services_provide.drop_indexes("*")
        print(db.services_provide.index_information())
        #db.create_collection('services_provide',{"autoindexid": False})
        db.services_provide.insert_one({"name":1,"id":1})
        #db.services_provide.create_index("id",unique=True)
        
        db.services_provide.drop_indexes()
        #db.services_provide.drop_search_index({'_id'})
    except:
        print("error")
    
    
    return db.services_provide.find()
def remove_services():
    db.services_provide.delete_many({})


datas = create_collections()
for data in datas:
    print(data)
