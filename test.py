import requests
import json
from pprint import pprint

url = "https://api.hubspot.com/chirp-frontend-external-na1-proxy/v1/gateway/com.hubspot.marketplace.profiles.rpc.ProfilesPublicRpc/getProfile?hs_static_app=ecosystem-marketplace-solutions-public-ui&hs_static_app_version=1.16741&clienttimeout=5000"

payload = {
    "slug": "avidly"  # Verify this key in DevTools
}

headers = {
    "content-type": "application/json",
    #"user-agent": "Mozilla/5.0 ...", # Use your browser's user agent
    # Add other headers like 'cookie' and 'x-hubspot-csrf-hubspotapi' from your browser
}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())

