
import requests
from pprint import pprint
import json

VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": "",
    "version": "5.124",
    "user_id": "405421050",
}

query = f'{VK_CONFIG["domain"]}/groups.get?access_token={VK_CONFIG["access_token"]}&user_id={VK_CONFIG["user_id"]}&extended=1&v={VK_CONFIG["version"]}'
r = requests.get(query)

with open('repo_ex2.json', 'w') as f:
    json.dump(r.json(), f)

with open('repo_ex2.json') as f:
    pprint(json.load(f))
