import requests

headers = {
    "":""
}
url = "https://ecosystem.hubspot.com/marketplace/solutions/all"

page = requests.get(url,headers,timeout=0.01)

page.