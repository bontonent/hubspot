import requests
import json
import random
from pprint import pprint
# Need refine for run from main.py

from json_parsing import comment
#import comment #for run only this .py


def parsing_product_page(code_payload, choose_agent):
  # Preparing
  url = "https://api.hubspot.com/chirp-frontend-external-na1-proxy/v1/gateway/com.hubspot.marketplace.profiles.rpc.ProfilesPublicRpc/getProfile?hs_static_app=ecosystem-marketplace-solutions-public-ui&clienttimeout=5000"
  header = {
      "content-type": "application/json",
      "User-Agent": str(choose_agent),
      "Coockie":"_cfuvid=6rG4fisgKo.xvGbvtQoLJgnbmD97TVLuDiAoTTrBAG0-1764668437139-0.0.1.1-604800000"}
  payload = {"slug": str(code_payload)}
  
  # Run get json script
  response = requests.post(url, headers = header, data = json.dumps(payload))
  products = response.json()

  # Return json script
  result = products['data']['result']
  comments = comment.comment(result['id'],choose_agent)

  return comments,result

# Test how work. Run this script
if __name__ == "__main__":
  code_payload = 'performars'
  user_agent = "explorer|Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"
  comments, parsing_data = parsing_product_page(code_payload,user_agent)
  pprint(comments)
  pprint(parsing_data)

