import requests
import json
from pprint import pprint

def services_provide():    
    # prepering
    header = {"":""}
    url = "https://app.hubspot.com/api/service-catalog/public/v1/services?language=en&hs_static_app=ecosystem-marketplace-solutions-public-ui"
    
    # get json script
    response = requests.get(url,header)
    result  = response.json()
    return result

# Test run. Run this script for see json
if __name__ == "__main__":
    pprint(services_provide())
    

