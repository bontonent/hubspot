import requests
import json
from pprint import pprint

def credentials():
    # prepering
    header = {"":""}
    url = "https://api.hubspot.com/credentials/consumers/v1/credential-definitions?type=CERTIFICATION&invalidateCache=true&enabled=true&hs_static_app=ecosystem-marketplace-solutions-public-ui&hs_static_app_version=1.16741"
    
    # get json
    response = requests.get(url,header)
    creadis = response.json()
    result = creadis['results']
    return result

# Run this .py script for see json script
if __name__ == "__main__":
    pprint(credentials())
