import requests
import json

payload = {
    'query': {
        'query_string': {
            'query': 'a96f2b10-1a94-4de6-a45c-03d2f18b29f8'
        }
    }
}

payload = {
    'query': {
        'query_string': {
            'query': 'a96f2b10-1a94-4de6-a45c-03d2f18b29f8',
            'default_field': 'elem_id'
        }
    }
}

payload = {
    'query': {
        'query_string': {
            'query': 'second',
            'default_field': 'title'
        }
    }
}

payload = {
    'query': {
        'query_string': {
            'query': 'second',
            'default_field': 'title'
        }
    }
}

payload = {
    'query': {
        'query_string': {
            'query': 'PASS',
            'default_field': 'status'
        }
    }
}


url = 'http://localhost:19200/element/_search'
params = {
    'pretty': 'true'
}

res = requests.post(url, json=payload, params=params)
print(f'status_code: {res.status_code}')
print(json.dumps(res.json(), indent=4))

