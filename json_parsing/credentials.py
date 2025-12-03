import requests
import json
from pprint import pprint

url = "https://api.hubspot.com/credentials/consumers/v1/credential-definitions?type=CERTIFICATION&invalidateCache=true&enabled=true&hs_static_app=ecosystem-marketplace-solutions-public-ui&hs_static_app_version=1.16741"
header = {"":""}

response = requests.get(url,header)

creadis = response.json()
for cready in creadis['results']:
    run_metadata = True
    metadatas = cready['id'],cready['metadata']
    for metadata in metadatas[1]:
        if str(metadata['language']) == "en":
            print(cready['id'],metadata['title'])
            run_metadata = False
            break
    if run_metadata:
        print(cready['id'],cready['internalName'])
