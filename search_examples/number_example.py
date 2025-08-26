#!/usr/bin/env python3
import requests
import json
import time

params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
index = 'number_index'
url = f'{server}/{index}'

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
if True:
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

# add mapping
if True:
    payload = {
        'properties': {
            'elem_id': {
                'type': 'keyword'
            },
            'step_type': {
                'type': 'keyword'
            },
            'title': {
                'type': 'text'
            },
            'timeout': {
                'type': 'long'
            },
            'timeout2': {
                'type': 'keyword'
            },
            'execution_user_input': {
                'properties': {
                    'timeout': {
                        'type': 'long'
                    },
                    'timeout2': {
                        'type': 'keyword'
                    },
                    'entries': {
                        'properties': {
                            'data_path': {
                                'type': 'keyword'
                            },
                            'command_string': {
                                'type': 'text'
                            },
                            'timeout': {
                                'type': 'long'
                            },
                            'timeout2': {
                                'type': 'keyword'
                            }
                        }
                    }
                }
            }
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
        'elem_id': elem_id,
        'step_type': 'COMMAND',
        'title': 'First command step',
        'timeout': 2,
        'timeout2': '2',
        'execution_user_input': {
            'timeout': 2,
            'timeout2': '2',
            'entries': [
                {
                    'data_path': 'TZ-A',
                    'command_string': 'mycommand,arg1,arg2',
                    'timeout': 2,
                    'timeout2': '2'
                }
            ]
        }
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

    elem_id = 'guid-102'
    payload = {
        'elem_id': elem_id,
        'step_type': 'COMMAND',
        'title': 'First command step',
        'timeout': 11,
        'timeout2': '11',
        'execution_user_input': {
            'timeout': 11,
            'timeout2': '11',
            'entries': [
                {
                    'data_path': 'TZ-A',
                    'command_string': 'mycommand,arg1,arg2',
                    'timeout': 11,
                    'timeout2': '11'
                }
            ]
        }
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

    elem_id = 'guid-103'
    payload = {
        'elem_id': elem_id,
        'step_type': 'COMMAND',
        'title': 'First command step',
        'timeout': 3,
        'timeout2': '3',
        'execution_user_input': {
            'timeout': 3,
            'timeout2': '3',
            'entries': [
                {
                    'data_path': 'TZ-A',
                    'command_string': 'mycommand,arg1,arg2',
                    'timeout': 3,
                    'timeout2': '3'
                }
            ]
        }
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

# Sleep a bit to wait for in
for i in range(5):
    status_code, result = get_all_doc()
    count = result['hits']['total']['value']
    if count < 3:
        print(f'Wait for indexing to complete. count: {count}')
        time.sleep(1)
    else:
        print(f'Indexing completed.')
        break

# query entry properties
if True:
    #
    payload = {
        'query': {
            'term': {
                'timeout': {
                    'value': 2
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['timeout'] == 2

    #
    payload = {
        'query': {
            'range': {
                'timeout': {
                    'gte': 3
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['timeout'] >= 2
    assert result['hits']['hits'][1]['_source']['timeout'] >= 2
    
    #
    payload = {
        'query': {
            'bool': {
                'filter': {
                    'range': {
                        'timeout': {
                            'gte': 0
                        }
                    }
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 3
    assert result['hits']['hits'][0]['_source']['timeout'] >= 0
    assert result['hits']['hits'][1]['_source']['timeout'] >= 0
    assert result['hits']['hits'][2]['_source']['timeout'] >= 0

    #
    payload = {
        'query': {
            'term': {
                'timeout': {
                    'value': 2
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['timeout'] == 2

    #
    payload = {
        'query': {
            'range': {
                'execution_user_input.timeout': {
                    'gte': 3
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['timeout'] >= 3
    assert result['hits']['hits'][1]['_source']['execution_user_input']['timeout'] >= 3

    #
    payload = {
        'query': {
            'range': {
                'execution_user_input.entries.timeout': {
                    'gte': 3
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['timeout'] >= 3
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['timeout'] >= 3

    #  This does not work
    '''
    payload = {
        'query': {
            'range': {
                'execution_user_input.entries[0].timeout': {
                    'gte': 3
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert status_code == 200
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['timeout'] >= 3
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['timeout'] >= 3
    '''