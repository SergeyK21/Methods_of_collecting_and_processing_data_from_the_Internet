import requests
from pprint import pprint
import json

username = "SergeyK21"

r = requests.get(f"https://api.github.com/users/{username}/repos")

with open('repo_ex1.json', 'w') as f:
    json.dump(r.json(), f)

with open('repo_ex1.json') as f:
    pprint(json.load(f))