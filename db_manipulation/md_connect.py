from pymongo import MongoClient
import os

def connect():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client.hubspot
        return db
    except Exception as e:
        return "disconect"

# service
def cc_services(db,datas):
    try:
        try:
            db.create_collection('services_provide')
        except:
            None
        db.services_provide.insert_many(datas)
        return "complete"
    except Exception as e:
        return e
def vc_services(db):
    return list(db.services_provide.find())
def rc_services(db):
    db.services_provide.delete_many({})

# credentials
def cc_credentials(db,datas):
    try:
        try:
            db.create_collection('credentials')
        except:
            None
        db.credentials.insert_many(datas)
        return "complete"
    except Exception as e:
        print(e)
        return e
def vc_credentials(db):
    return list(db.credentials.find())
def rc_credentials(db):
    db.credentials.delete_many({})

# products
def cc_products(db,datas):
    try:
        try:
            db.create_collection('products')
        except:
            None
        db.products.insert_many(datas)
        return "complete"
    except Exception as e:
        return e
def vc_products(db):
    return list(db.products.find())
def rc_products(db):
    db.products.delete_many({})



if __name__ == "__main__":
    datas = [{"name":2,"_id":2},{"name":1,"_id":1}]
    db = connect()
    rc_credentials(db)
    rc_services(db)

