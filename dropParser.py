import requests
import config
import json

def getDropJSON(url):
    response = requests.get(url, headers = config.HEADERS)
    with open('solDrop.json', 'w') as f:
        json.dump(response.json(), f)

getDropJSON(config.HOWRAREISAPI)