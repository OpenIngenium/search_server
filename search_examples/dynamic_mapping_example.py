#!/usr/bin/env python3
import requests
import json
import time
import sys
params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
index = 'dynamic'
url = f'{server}/{index}'

def create_index():
    print(f'url: {url}')
    res = requests.get(url, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    if res.status_code == 200:
        print(f'Delete index: {index}')
        res = requests.delete(url, params=params)
        print(f'status_code: {res.status_code}')
        print(json.dumps(res.json(), indent=4))
        assert res.status_code == 200

    print(f'Creating index: {index}')
    res = requests.put(url, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 200

def print_index_info():
    res = requests.get(url, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

def get_all_doc():
    res = requests.get(f'{url}/_search', params=params)
    return res.status_code, res.json()

def print_doc(id):
    res = requests.get(f'{url}/_doc/{id}', params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

def do_search(payload):
    res = requests.get(f'{url}/_search', json=payload, params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    return res.status_code, res.json()

def get_mapping():
    res = requests.get(f'{url}/_mapping', params=params)

    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    return res.status_code, res.json()

# create index
create_index()

# add mapping
if True:
    payload = {
        'dynamic_templates': [
            {
                'string_as_wildcard': {
                    'match_mapping_type': 'string',
                    'mapping': {
                        'type': 'wildcard'
                    }
                },
            },
            {
                'start_time': {
                    'match_mapping_type': 'string',
                    'match': 'start_time',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'time_prefix': {
                    'match_mapping_type': 'string',
                    'match': 'time_*',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'time_postfix': {
                    'match_mapping_type': 'string',
                    'match': '*_time',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'ert': {
                    'match_mapping_type': 'string',
                    'match': 'ert',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'scet': {
                    'match_mapping_type': 'string',
                    'match': 'scet',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'scet': {
                    'match_mapping_type': 'string',
                    'match': 'scet',
                    'mapping': {
                        'type': 'date'
                    }
                },
            },
            {
                'started_on': {
                    'match_mapping_type': 'string',
                    'match': 'started_on',
                    'mapping': {
                        'type': 'date'
                    }
                },
            }   
        ]
    }

    res = requests.put(f'{url}/_mapping', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 200

    print_index_info()

# add a document
if True:
    elem_id = 'guid-101'
    payload = {
        'step_type': 'WAIT',
        'start_time': '2023-06-26T19:39:35.947Z',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    print_doc(id)

    elem_id = 'guid-102'
    payload = {
        'step_type': 'NAMUAL_INPUT',
        'start_time': '2023-06-27T19:39:35.947Z',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    print_doc(id)

    elem_id = 'guid-103'
    payload = {
        'step_type': 'WAIT',
        'start_time': '2023-06-28T19:39:35.947Z',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    print_doc(id)

    # This won't work
    elem_id = 'guid-104'
    payload = {
        'step_type': 'WAIT',
        'start_time': '',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 400

    # This works. 0 is the Linux epoch time
    elem_id = 'guid-104'
    payload = {
        'step_type': 'MANUAL_INPUT',
        'start_time': 0,
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    # This works. null is not indexed
    elem_id = 'guid-105'
    payload = {
        'step_type': 'WAIT',
        'start_time': None,
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

# Sleep a bit to wait for indexing to complete
for i in range(5):
    status_code, result = get_all_doc()
    count = result['hits']['total']['value']
    if count < 3:
        print(f'Wait for indexing to complete. count: {count}')
        time.sleep(1)
    else:
        print(f'Indexing completed.')
        break

# query
if True:
    #
    ref_time = '2023-06-27T19:39:35.947'
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['start_time'] >= ref_time
    assert result['hits']['hits'][1]['_source']['start_time'] >= ref_time

    #
    ref_time = '2023-06-01T19:39:35.947'
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'lt': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['start_time'] == 0
    
    get_mapping()
    