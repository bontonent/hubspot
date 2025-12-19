import requests
import json
from pprint import pprint

def comment(code_product, choose_agent):
    # preparing
    datas = []
    search_one_time = 100 # less than or equal 100 
    get_data = 0; page = 1
    
    # Geting each data from him
    run_parsing = True
    while run_parsing:
        total_message, data = parsing_ones(code_product,choose_agent,page,search_one_time,get_data)
        get_data += search_one_time
        datas += data
        if total_message <= get_data:
            run_parsing = False
    return datas
            
def parsing_ones(code_product, choose_agent,page,search_one_time,get_data):
    # Preparing
    url = "https://api.hubspot.com/ecosystem/public/v1/reviews/search?hs_static_app=ecosystem-marketplace-solutions-public-ui"
    header = {
        "content-type": "application/json",
        "User-Agent": choose_agent,
        "Coockie": "_cfuvid=6rG4fisgKo.xvGbvtQoLJgnbmD97TVLuDiAoTTrBAG0-1764668437139-0.0.1.1-604800000"}

    payload = {
        "limit": search_one_time    # limit search one time
        ,"page": page               # id_page
        ,"entityId": code_product    # id product
        ,"sortFields": ["NEWEST"]
        ,"offset": get_data          # already get data
        ,"language": "en"
        ,"reviewTypes": ["PROFILE"]
    }

    # Run get json script
    response = requests.post(url, headers = header, data = json.dumps(payload))
    products = response.json()
    # Return json script
    
    result = products['reviews']
    total_message = products['total']
    return total_message,result

# Test how work. Run this script
if __name__ == "__main__":
  code_product = 2468
  #code_product = 834
  user_agent = "explorer|Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"
  items = comment(code_product,user_agent)
  pprint(items)
  print(len(items))
