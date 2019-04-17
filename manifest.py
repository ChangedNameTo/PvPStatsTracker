import requests
import json
import time

headers  = {'X-API-Key' : '53bd4b2f43ba42ab93608343956cd09b'}
base_url = 'https://www.bungie.net/Platform'

manifest = '/Destiny2/Manifest/'
r        = requests.get(base_url + manifest, headers = headers).content

print(r)

content = 'http://www.bungie.net/common/destiny2_content/json/en/aggregate-384d762f-d90e-4d6d-b10e-304f2956c59e.json'
# r        = requests.get(content, headers = headers).content

# print(r)
