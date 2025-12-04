from json_parsing import credentials            # in nothing; out json
from json_parsing import services_provide       # in nothing; out json
from json_parsing import parsing_product_page   # in code_search, user_agent; out comments, json
from json_parsing import catalog_parsing        # in user_agent; out code_search

from user_agents import user_agents             # in nothing; out user_agents

from random import randrange
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint


class main_script:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        user_agent = user_agents.get_agent("/".join([str(BASE_DIR),"user_agents"]))
        self.choose_user = str(user_agent[randrange(1,len(user_agent)-1)])
        self.products = []
        
    
    def main(self):
        # future = {}
        # codes = catalog_parsing.catalog_parsing(self.choose_user, 1)
        #print(codes[0])

        # with ThreadPoolExecutor(10) as thread:
        #     for code in tqdm(codes):
        #         future[thread.submit(parsing_product_page.parsing_product_page, code, self.choose_user)] = code
        #     for fut in tqdm(as_completed(future),total=len(future)):
        #         try:
        #             self.products.append(fut.result(timeout=3))
        #         except:
        #             for n in range(2):
        #                 try:
        #                     self.products.append(fut.result(timeout=3))
        #                     break
        #                 except:
        #                     continue

        service = services_provide.services_provide()
        pprint(service)
        # creden = credentials.credentials()
        # print(creden)



if __name__ == "__main__":
    class_main = main_script()
    class_main.main()
