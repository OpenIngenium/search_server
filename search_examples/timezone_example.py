#!/usr/bin/env python3
import requests
import json
import time
import sys
params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
index = 'timestamp_index'
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

# create index
create_index()

# add mapping
if True:
    payload = {
        'properties': {
            'start_time': {
                'type': 'date',
                'format': 'strict_date_optional_time',
            },
        }
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
        'start_time': '2023-07-01T10:00:00.000Z',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    elem_id = 'guid-102'
    payload = {
        'start_time': '2023-07-01T10:00:00.000',   # treated as UTC
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    elem_id = 'guid-103'
    payload = {
        'start_time': '2023-07-01T10:00:00.000PST',   # ES will fail to parse this
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 400

    elem_id = 'guid-103'
    payload = {
        'start_time': '2023-07-01T10:00:00.000-0700',
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))
    assert res.status_code == 201

    elem_id = 'guid-104'
    payload = {
        'start_time': '2023-07-01T17:00:00.000Z',
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
    ref_time = '2023-07-01T10:00:00.000'     # ES treats this as UTC
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time,
                    'lte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['start_time'] == '2023-07-01T10:00:00.000Z'
    assert result['hits']['hits'][1]['_source']['start_time'] == '2023-07-01T10:00:00.000'

    #
    ref_time = '2023-07-01T10:00:00.000Z'
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time,
                    'lte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['start_time'] == '2023-07-01T10:00:00.000Z'
    assert result['hits']['hits'][1]['_source']['start_time'] == '2023-07-01T10:00:00.000'

    #
    ref_time = '2023-07-01T10:00:00.000PST'    # ES gives an error for this
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time,
                    'lte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 400
    
    #
    ref_time = '2023-07-01T17:00:00.000'
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time,
                    'lte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_id'] == 'guid-103'
    assert result['hits']['hits'][0]['_source']['start_time'] == '2023-07-01T10:00:00.000-0700'
    assert result['hits']['hits'][1]['_id'] == 'guid-104'
    assert result['hits']['hits'][1]['_source']['start_time'] == '2023-07-01T17:00:00.000Z'

    #
    ref_time = '2023-07-01T10:00:00.000-0700'
    payload = {
        'query': {
            'range': {
                'start_time': {
                    'gte': ref_time,
                    'lte': ref_time
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_id'] == 'guid-103'
    assert result['hits']['hits'][0]['_source']['start_time'] == '2023-07-01T10:00:00.000-0700'
    assert result['hits']['hits'][1]['_id'] == 'guid-104'
    assert result['hits']['hits'][1]['_source']['start_time'] == '2023-07-01T17:00:00.000Z'