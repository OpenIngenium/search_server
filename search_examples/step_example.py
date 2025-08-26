#!/usr/bin/env python3
import requests
import json
import time
params = {
    'pretty': 'true'
}

server = 'http://localhost:19200'
index = 'step_index'
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
            'elem_id': {
                'type': 'keyword'
            },
            'step_type': {
                'type': 'keyword'
            },
            'title': {
                'type': 'text'
            },
            'execution_user_input': {
                'properties': {
                    'entries': {
                        'properties': {
                            'data_path': {
                                'type': 'keyword'
                            },
                            'data_path2': {
                                'type': 'text'
                            },
                            'command_string': {
                                'type': 'text'
                            },
                            'command_string2': {
                                'type': 'wildcard'
                            },
                            'evrs': {
                                "properties": {
                                    'name': {
                                        'type': 'keyword'
                                    }
                                }
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

    print_index_info()

# add a document
if True:
    elem_id = 'guid-101'
    payload = {
        'elem_id': elem_id,
        'step_type': 'COMMAND',
        'title': 'First command step',
        'execution_user_input': {
            'entries': [
                {
                    'data_path': 'TZ-A',
                    'data_path2': 'TZ-A',
                    'command_string': 'mycommand,arg1,arg2',
                    'command_string2': 'mycommand,arg1,arg2',
                    'evrs': {
                        'name': 'EVR1',
                    }
                },
                {
                    'data_path': 'TZ-B',
                    'data_path2': 'TZ-B',
                    'command_string': 'mycommand2,arg1,arg2',
                    'command_string2': 'mycommand2,arg1,arg2',
                    'evrs': {
                        'name': 'EVR2',
                    }
                }
            ]
        }
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

if True:
    elem_id = 'guid-102'
    payload = {
        'elem_id': elem_id,
        'step_type': 'COMMAND',
        'title': 'Second command step',
        'execution_user_input': {
            'entries': [
                {
                    'data_path': 'TZ-B',
                    'data_path2': 'TZ-B',
                    'command_string': 'yourcommand,arg1,arg2',
                    'command_string2': 'yourcommand,arg1,arg2',
                    'evrs': {
                        'name': 'EVR1',
                    }
                },
                {
                    'data_path': 'TZ-B',
                    'data_path2': 'TZ-B',
                    'command_string': 'yourcommand2,arg1,arg2',
                    'command_string2': 'yourcommand2,arg1,arg2',
                    'evrs': {
                        'name': 'EVR4',
                    }
                }
            ]
        }
    }
    id = elem_id
    res = requests.put(f'{url}/_create/{id}', json=payload, params=params)
    print(f'status_code: {res.status_code}')
    print(json.dumps(res.json(), indent=4))

    print_doc(id)

# Sleep a bit to wait for indexing to complete
for i in range(5):
    status_code, result = get_all_doc()
    count = result['hits']['total']['value']
    if count < 2:
        print(f'Wait for indexing to complete. count: {count}')
        time.sleep(1)
    else:
        print(f'Indexing completed.')
        break

# query entry properties
if True:
    payload = {
        'query': {
            'term': {
                'execution_user_input.entries.data_path': {
                    'value': 'TZ-A'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-A'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    #
    payload = {
        'query': {
            'term': {
                'execution_user_input.entries.data_path': {
                    'value': 'TZ-B'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-A'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    #
    payload = {
        'query': {
            'term': {
                'execution_user_input.entries.evrs.name': {
                    'value': 'EVR1'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-A'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    #
    payload = {
        'query': {
            'term': {
                'execution_user_input.entries.evrs.name': {
                    'value': 'EVR4'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    # match query
    payload = {
        'query': {
            'match': {
                'execution_user_input.entries.data_path2': 'TZ'
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-A'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    # match query
    payload = {
        'query': {
            'match': {
                'execution_user_input.entries.data_path2': 'TZ-A'
            }
        }
    }
    status_code, result = do_search(payload)
    # note that the query will return TZ-B as well probably because the query text is tokenized
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-A'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['data_path'] == 'TZ-B'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['data_path'] == 'TZ-B'

    # match query
    payload = {
        'query': {
            'match': {
                'execution_user_input.entries.command_string': 'yourcommand2,arg1,arg2'
            }
        }
    }
    status_code, result = do_search(payload)
    # This matches both yourcommand, yourcommand2, mycommand, mycommand2
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['command_string'] == 'yourcommand,arg1,arg2'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['command_string'] == 'yourcommand2,arg1,arg2'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['command_string'] == 'mycommand,arg1,arg2'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['command_string'] == 'mycommand2,arg1,arg2'

    # wildcard query
    payload = {
        'query': {
            'wildcard': {
                'execution_user_input.entries.command_string2': {
                    'value': 'yourcommand2,arg1,arg2'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['command_string'] == 'yourcommand,arg1,arg2'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['command_string'] == 'yourcommand2,arg1,arg2'

    # wildcard query. No partial match
    payload = {
        'query': {
            'wildcard': {
                'execution_user_input.entries.command_string2': {
                    'value': 'arg1,arg2'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 0

    # wildcard query. use wildcard
    payload = {
        'query': {
            'wildcard': {
                'execution_user_input.entries.command_string2': {
                    'value': '*arg1,arg*'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 2
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['command_string'] == 'mycommand,arg1,arg2'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['command_string'] == 'mycommand2,arg1,arg2'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][0]['command_string'] == 'yourcommand,arg1,arg2'
    assert result['hits']['hits'][1]['_source']['execution_user_input']['entries'][1]['command_string'] == 'yourcommand2,arg1,arg2'

    # wildcard query. use wildcard in the middle
    payload = {
        'query': {
            'wildcard': {
                'execution_user_input.entries.command_string2': {
                    'value': '*mycommand,*arg1*'
                }
            }
        }
    }
    status_code, result = do_search(payload)
    assert result['hits']['total']['value'] == 1
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][0]['command_string'] == 'mycommand,arg1,arg2'
    assert result['hits']['hits'][0]['_source']['execution_user_input']['entries'][1]['command_string'] == 'mycommand2,arg1,arg2'
