import requests
import json
from pprint import pprint

header = {
    "":""
}

url = "https://app.hubspot.com/api/service-catalog/public/v1/services?language=en&hs_static_app=ecosystem-marketplace-solutions-public-ui&hs_static_app_version=1.16741"


response = requests.get(url,header)

services  = response.json()
for service in services:
    print(service['id'], service['name'])

