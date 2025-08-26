#!/usr/bin/env python3
import requests
import json
params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
index = 'hk_index'
url = f'{server}/{index}'

def print_index_info():
    res = requests.get(url, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

def print_doc(id):
    res = requests.get(f'{url}/_doc/{id}', params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

def do_search(payload):
    res = requests.get(f'{url}/_search', json=payload, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    return res.status_code, res.json()

# create index
if False:
    print(f'url: {url}')
    res = requests.get(url, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    if res.status_code == 404:
        print(f'Creating index: {index}')
        res = requests.put(url, params=params)
        print(f'status_code: {res.status_code}')
        print(json.dumps(res.json(), indent=4))

# add mapping
if False:
    payload = {
        'properties': {
            'state_name': {
                'type': 'keyword'
            }
        }
    }

    res = requests.put(f'{url}/_mapping', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))


# put updates mapping instead of replacing
if False:
    payload = {
        'properties': {
            'motto': {
                'type': 'text'
            }
        }
    }
    res = requests.put(f'{url}/_mapping', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_index_info()

# mapping for nested properties
if False:
    payload = {
        'properties': {
            'meta_data': {
                'properties': {
                    'postal_code': {
                        'type': 'keyword'
                    }
                }
            }
        }
    }
    res = requests.put(f'{url}/_mapping', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_index_info()

# add a document
if False:
    payload = {
        'state_name': 'North Carolina',
        'motto': 'To Be rather than To Seem'
    }
    id = 'nc'
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

# add a document
if False:
    payload = {
        'state_name': 'North Dakota',
        'motto': 'Liberty and Union Be Now and Forever'
    }
    id = 'nd'
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

# add a document with nested properties
if False:
    payload = {
        'state_name': 'New Jersey',
        'motto': 'Liberty and Prosperity',
        'meta_data': {
            'postal_code': 'NJ'
        }
    }
    id = 'nj'
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

if False:
    payload = {
        'query': {
            'term': {
                'state_name': {
                    'value': 'North Dakota'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

    # By default, search is case sensitive
    payload = {
        'query': {
            'term': {
                'state_name': {
                    'value': 'North dakota'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # case insensitive search
    payload = {
        'query': {
            'term': {
                'state_name': {
                    'value': 'North dakota',
                    'case_insensitive': True
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

    # partial match is not supported for term search
    payload = {
        'query': {
            'term': {
                'state_name': {
                    'value': 'North'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # wild card is not supported for term search
    payload = {
        'query': {
            'term': {
                'state_name': {
                    'value': 'North*'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # use wildcard explicitly
    payload = {
        'query': {
            'wildcard': {
                'state_name': 'North*'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2

    # use wildcard explicitly
    payload = {
        'query': {
            'wildcard': {
                'state_name': '*orth *'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2

    # wildcard and case sensitive
    payload = {
        'query': {
            'wildcard': {
                'state_name': '*orTh *'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # wildcard and case sensitive
    payload = {
        'query': {
            'wildcard': {
                'state_name': {
                    'value': '*orTh *',
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # wildcard and case sensitive
    payload = {
        'query': {
            'wildcard': {
                'state_name': {
                    'value': '*orTh *',
                    'case_insensitive': False
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # wildcard and case insensitive
    payload = {
        'query': {
            'wildcard': {
                'state_name': {
                    'value': '*orTh *',
                    'case_insensitive': True
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2


if False:
    # use term on text won't match
    payload = {
        'query': {
            'term': {
                'motto': {
                    'value': 'rather Than'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # use match on text. case in-sensitive
    payload = {
        'query': {
            'match': {
                'motto': 'raTher Than'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

    # use match on text. case in-sensitive. 'raTher' matches
    payload = {
        'query': {
            'match': {
                'motto': 'raTher sEE'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

    # use match on text. case in-sensitive. 'seeM' matches.
    payload = {
        'query': {
            'match': {
                'motto': 'seeM'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

    # use match on text. case in-sensitive. no token match
    payload = {
        'query': {
            'match': {
                'motto': 'see'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

# query nested properties
if True:
    payload = {
        'query': {
            'term': {
                'postal_code': {
                    'value': 'NJ'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    payload = {
        'query': {
            'term': {
                'meta_data.postal_code': {
                    'value': 'NJ'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1

