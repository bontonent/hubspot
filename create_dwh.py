from db_manipulation import pd_connect
from db_manipulation import md_connect
from pprint import pprint

class datawarehouse:
    def __init__(self):
        self.db = md_connect.connect()
    def main(self):
        pprint(md_connect.vc_products(self.db)[100])
        
        self.get_data_credentials()
        self.get_data_services()
    
    def get_data_credentials(self):
        results = []
        datas = md_connect.vc_credentials(self.db)
        for data in datas:
            result = {
                "id": data['_id']
                ,"title": None
                }
            metadatas = data['metadata']
            for metadata in metadatas:
                if metadata['language'] == 'en':
                    result['title'] = metadata['title']
            results.append(result)
        return results
    
    def get_data_services(self):
        results = []
        datas = md_connect.vc_services(self.db)
        for data in datas[:3]:
            result = {
                "id": data['_id']
                ,"name": data['name']
            }
            results.append(result)
        return results


if __name__ == "__main__":
    class_dwh = datawarehouse()
    class_dwh.main()
