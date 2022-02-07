import requests
import config
import json

def getDropJSON(url, filename):
    response = requests.get(url, headers = config.HEADERS)
    with open(filename, 'w') as f:
        json.dump(response.json(), f)

getDropJSON(config.HOWRAREISAPI, 'solDrop.json')
getDropJSON(config.MAGICEDENAPI, 'magicDrop.json')
