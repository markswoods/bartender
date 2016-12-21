import requests
import json

resp = json.loads(requests.get("http://localhost:5000/pilsners").text)
print json.dumps(resp, indent=4, separators=(',', ':'))

for beer in resp:
    print beer['brewer'], beer['product']