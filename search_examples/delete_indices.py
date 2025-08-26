#!/usr/bin/env python3
import requests
import json
params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
indices = ['syncdata', 'querybuilder', 'element', 'procedure_element']

for index in indices:
    url = f'{server}/{index}'
    res = requests.delete(url, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
