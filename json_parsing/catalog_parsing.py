import requests
import json
from pprint import pprint
from tqdm import tqdm

def catalog_parsing(choose_agent, times = 0):
    # preparing
    datas = []
    search_one_time = 100 # less than or equal 100 
    get_data = 0; 
    
    # Geting each data from him
    first_print = True
    while True:
        total_products, data = parsing_ones(choose_agent,search_one_time,get_data)
        get_data += search_one_time
        datas += data
        if total_products <= get_data:
            break
        elif (times > 0):
            if get_data/100 > times-1:
                break

        # Understnad how much
        if first_print:
            print(total_products)
            first_print=False
        
    return datas

def parsing_ones(choose_agent,search_one_time,get_data):
    url = "https://api.hubspot.com/marketplace-search/public/v1/profiles/search?hs_static_app=ecosystem-marketplace-solutions-public-ui"
    url = "https://api.hubspot.com/marketplace-search/public/v1/profiles/search?hs_static_app=ecosystem-marketplace-solutions-public-ui"
    header = {
        "content-type": "application/json"
        , "cookie": "FPID=FPID2.2.ESKmdi6Vf%2FpROH2SyMwci5%2FtwZoSMT64fIFBaFrWg%2Fo%3D.1764165959; _gtmeec=e30%3D; __hs_cookie_cat_pref=1:false_2:false_3:false; _cfuvid=FVZsw.AvLKDPoI6Cqqp8UplauVfX9oxmmYAuLBnbn.4-1764751961762-0.0.1.1-604800000; __cf_bm=wdKJOJDA.0E4DSMUGsLop2ZZJAnYryr_FF8WGm8H94s-1764762200-1.0.1.1-OcGmT4ct_HRBW0wPBX8pF4My9sC57sHoUTUBG9mVg9xAg5rXekLa6F6Pn5bxybs1EgO4Vyp4VjxeBu1CQnJ4sRtHxnJKaXLYdfJH5.pxb0U"
        , "User-Agent": choose_agent
    }
    payload = [{
        "sorts":[{"sortField":"PARTNER_TIER","sortOrder":"DESC"}
        , {"sortField":"PARTNER_TYPE","sortOrder":"ASC"}
        , {"sortField":"RELEVANCE","sortOrder":"DESC"}
        , {"sortField":"REVIEW_COUNT","sortOrder":"DESC"}
        , {"sortField":"CREATED_AT","sortOrder":"ASC"}]
        , "offset":get_data
        , "limit":search_one_time
        , "callingUserLanguage":"en"
    }]
    # payload = [{
    #     "budgetsFilter":{"clause":"OR"
    #         ,"values":["NONE"]}
    #         ,"sorts":[
    #     {"sortField":"PARTNER_TIER","sortOrder":"DESC"}
    #     ,{"sortField":"PARTNER_TYPE","sortOrder":"ASC"}
    #     ,{"sortField":"RELEVANCE","sortOrder":"DESC"}
    #     ,{"sortField":"REVIEW_COUNT","sortOrder":"DESC"}
    #     ,{"sortField":"CREATED_AT","sortOrder":"ASC"}]
    #     , "offset":get_data
    #     ,"limit":search_one_time,"callingUserLanguage":"en"}]

    response = requests.post(url, headers=header, data = json.dumps(payload))
    response_json = response.json()[0]
    total = response_json['total']
    products = response_json['items']
    products_slug = []
    
    for product in products:
        products_slug.append(product['slug'])

    return total,products_slug


# Test how work. Run this script
if __name__ == "__main__":
  user_agent = "explorer|Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"
  items = catalog_parsing(user_agent)
  pprint(items)
  print(len(items))

