from json_parsing import credentials            # in nothing; out json
from json_parsing import services_provide       # in nothing; out json
from json_parsing import parsing_product_page   # in code_search, user_agent; out comments, json
from json_parsing import catalog_parsing        # in user_agent; out code_search

from db_manipulation import md_connect

from user_agents import user_agents             # in nothing; out user_agents

from random import randrange
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

import sys


class main_script:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        user_agent = user_agents.get_agent("/".join([str(BASE_DIR),"user_agents"]))
        self.choose_user = str(user_agent[randrange(1,len(user_agent)-1)])
        self.products = []
    
    def main(self):
        db = md_connect.connect()
        if str(db) == "disconect":
            sys.exit()
        future = {}
        codes = catalog_parsing.catalog_parsing(self.choose_user)
        # codes = catalog_parsing.catalog_parsing(self.choose_user, 1) # run only first
        
        md_connect.rc_products(db)
        with ThreadPoolExecutor(5) as thread:
            for code in tqdm(codes):
                future[thread.submit(parsing_product_page.parsing_product_page, code, self.choose_user)] = code
            for fut in tqdm(as_completed(future),total=len(future)):
                try:
                    comments,result = fut.result(timeout=3)
                except:
                    for n in range(2):
                        try:
                            retry_res = thread.submit(parsing_product_page.parsing_product_page, code,self.choose_user).result(timeout=3)
                            comments, result = fut.result(timeout=3)
                        except Exception as e:
                            print(e)
                            continue
                result["comment"] = comments
                result["_id"] = result.pop("id")
                md_connect.cc_products(db, [result])
        
        md_connect.rc_services(db)
        services = services_provide.services_provide()
        for service in tqdm(services):
            service["_id"] = service.pop("id")
            md_connect.cc_services(db,[service])
            
        md_connect.rc_credentials(db)
        credens = credentials.credentials()
        for creden in tqdm(credens):
            #print(creden)
            creden["_id"] = creden.pop("id")
            md_connect.cc_credentials(db, [creden])        
        # pprint(creden)



if __name__ == "__main__":
    class_main = main_script()
    class_main.main()
