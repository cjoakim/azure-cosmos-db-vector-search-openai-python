"""
Usage:
    python cogsearch_main.py display_config
    -
    python cogsearch_main.py create_cosmos_nosql_datasource <db> <collection>
    python cogsearch_main.py create_cosmos_nosql_datasource dev airports --no-http
    python cogsearch_main.py create_cosmos_nosql_datasource dev airports
    python cogsearch_main.py create_cosmos_nosql_datasource dev routes
    -
    python cogsearch_main.py create_cosmos_nosql_datasource <acct-env-var> <key-env-var> <dbname> <container-name>
    python cogsearch_main.py create_cosmos_nosql_datasource AZURE_COSMOSDB_NOSQL_ACCT AZURE_COSMOSDB_NOSQL_RO_KEY1 dev baseballplayers
    -
    python cogsearch_main.py delete_datasource <name>
    python cogsearch_main.py delete_datasource create_cosmos_nosql_datasource
    -
    python cogsearch_main.py list_indexes
    python cogsearch_main.py list_indexers
    python cogsearch_main.py list_datasources
    -
    python cogsearch_main.py get_xxx <name>
    python cogsearch_main.py get_index baseballplayers
    python cogsearch_main.py get_indexer baseballplayers
    python cogsearch_main.py get_indexer_status baseballplayers
    python cogsearch_main.py get_datasource cosmosdb-nosql-dev-baseballplayers
    -
    python cogsearch_main.py create_index <index_name> <schema_file>
    python cogsearch_main.py create_index baseballplayers baseballplayers_index.json
    python cogsearch_main.py delete_index baseballplayers
    -
    python cogsearch_main.py create_indexer <indexer_name> <schema_file>
    python cogsearch_main.py create_indexer baseballplayers baseballplayers_indexer.json
    python cogsearch_main.py delete_indexer baseballplayers
    python cogsearch_main.py run_indexer baseballplayers
    -
    python cogsearch_main.py create_searches_json
    python cogsearch_main.py list_searches_json
    -
    python cogsearch_main.py search_index <index_name> <searches-json-key>
    python cogsearch_main.py search_index baseballplayers all_players 
    python cogsearch_main.py search_index baseballplayers aaronha01
    -
    python cogsearch_main.py vector_search_like baseballplayers aaronha01
    -
    python cogsearch_main.py lookup_doc baseballplayers eVBWc0FPdExvZzJYQXdBQUFBQUFBQT090
"""

import base64
import json
import sys
import time
import os
import traceback

from docopt import docopt

from pysrc.cogbundle import Bytes, CogSearchClient, CogSvcsClient, Counter, Env, FS, OpenAIClient, Storage, System

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def new_client():
    opts = {}
    opts['name'] = os.environ['AZURE_SEARCH_NAME']
    opts['url'] = os.environ['AZURE_SEARCH_URL']
    opts['admin_key'] = os.environ['AZURE_SEARCH_ADMIN_KEY']
    opts['query_key'] = os.environ['AZURE_SEARCH_QUERY_KEY']
    return CogSearchClient(opts)

def create_searches_json():
    data = {}
    s1 = {}
    #s1['name'] = 'all_players'
    s1['count'] = "true"
    s1['search'] = "*"
    s1['orderby'] = "playerID"
    s1['select'] = 'id,playerID,nameFirst,nameLast,primary_position,embeddings_str'
    data['all_players'] = s1

    pids = 'aaronha01,jeterde01,henderi01,blombro01,guidrro01,rosepe01'.split(',')
    attrs = 'id,playerID,nameFirst,nameLast,primary_position,embeddings_str'
    for pid in pids:
        key1 = f'{pid}'
        key2 = f'{pid}_full'
        data[key1] = create_search_json_for_player(pid, attrs)
        data[key2] = create_search_json_for_player(pid, '*')
    FS.write_json(data, searches_json_file())

def create_search_json_for_player(pid, select_attrs):
    s = {}
    #s['name'] = pid
    s['count'] = "true"
    s['search'] = "playerID eq '{}'".format(pid)
    s['orderby'] = "playerID"
    s['select'] = select_attrs
    return s

def load_json_file(infile):
    with open(infile, 'rt') as json_file:
        return json.loads(str(json_file.read()))

def searches_json_file():
    return 'cogsearch_searches.json'

def vector_search_like(client, index_name, pid):
    # First do a lookup search for the given playerID
    lookup_name = f'lookup_{pid}'
    lookup_params = {}
    lookup_params['count'] = "true"
    lookup_params['search'] = "playerID eq '{}'".format(pid)
    lookup_params['orderby'] = "playerID"
    lookup_params['select'] = 'id,playerID,nameFirst,nameLast,primary_position,embeddings_str,embeddings'
    r = client.search_index(index_name, lookup_name, lookup_params)
    if r.status_code == 200:
        print(f'lookup search successful for player: {pid}')
        resp_obj = json.loads(r.text)
        if 'value' in resp_obj.keys():
            value = resp_obj['value']
            if len(value) > 0:
                # Next do a lookup search for the given playerID
                embeddings = value[0]['embeddings']
                vector = {}
                vector['value'] = embeddings
                vector['fields'] = 'embeddings'
                vector['k'] = 10
                vector_params = {}
                vector_params['count'] = "true"
                vector_params['select'] = 'id,playerID,nameFirst,nameLast,primary_position'
                vector_params['orderby'] = "playerID"
                vector_params['vectors'] = [ vector ]
                print(json.dumps(vector_params, sort_keys=False, indent=2))
                
                lookup_name = f'vector_{pid}'
                r = client.search_index(index_name, lookup_name, vector_params)
                if r.status_code == 200:
                    resp_obj = json.loads(r.text)
                    print(json.dumps(resp_obj, sort_keys=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options('Error: missing function')
        sys.exit(1)

    try:
        print(sys.argv)
        func = sys.argv[1].lower()
        client = new_client()

        if func == 'display_config':
            client.display_config()

        elif func == 'list_indexes':
            client.list_indexes()

        elif func == 'list_indexers':
            client.list_indexers()

        elif func == 'list_datasources':
            client.list_datasources()

        elif func == 'get_index':
            name = sys.argv[2]
            client.get_index(name)

        elif func == 'get_indexer':
            name = sys.argv[2]
            client.get_indexer(name)

        elif func == 'get_indexer_status':
            name = sys.argv[2]
            client.get_indexer_status(name)

        elif func == 'get_datasource':
            name = sys.argv[2]
            client.get_datasource(name)

        elif func == 'create_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_index(index_name, schema_file)

        elif func == 'update_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_index(index_name, schema_file)

        elif func == 'delete_index':
            name = sys.argv[2]
            client.delete_index(name)

        elif func == 'create_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_indexer(indexer_name, schema_file)

        elif func == 'update_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_indexer(indexer_name, schema_file)

        elif func == 'delete_indexer':
            name = sys.argv[2]
            client.delete_indexer(name)

        elif func == 'reset_indexer':
            name = sys.argv[2]
            client.reset_indexer(name)

        elif func == 'run_indexer':
            name = sys.argv[2]
            client.run_indexer(name)

        elif func == 'create_cosmos_nosql_datasource':
            acct_envvar = sys.argv[2]
            key_envvar  = sys.argv[3]
            dbname      = sys.argv[4]
            container   = sys.argv[5]
            client.create_cosmos_nosql_datasource(acct_envvar, key_envvar, dbname, container)

        elif func == 'delete_datasource':
            name = sys.argv[2]
            client.delete_datasource(name)

        elif func == 'create_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_synmap(synmap_name, schema_file)

        elif func == 'update_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_synmap(synmap_name, schema_file)

        elif func == 'delete_synmap':
            synmap_name = sys.argv[2]
            client.delete_synmap(synmap_name)

        elif func == 'search_index':
            index_name = sys.argv[2]
            search_name = sys.argv[3]
            searches = load_json_file(searches_json_file())
            if search_name in searches.keys():
                search_config = searches[search_name]
                if len(sys.argv) > 4:
                    additional = sys.argv[4]
                r = client.search_index(index_name, search_name, search_config)
                if r.status_code == 200:
                    resp_obj = json.loads(r.text)
                    print(json.dumps(resp_obj, sort_keys=False, indent=2))
                else:
                    print(f"search status code: {r.status_code}")
            else:
                print('Error: search name not found: {} in {}'.format(search_name, searches_json_file()))

        elif func == 'vector_search_like':
            index_name, pid = sys.argv[2], sys.argv[3]
            vector_search_like(client, index_name, pid)

        elif func == 'create_searches_json':
            create_searches_json()

        elif func == 'list_searches_json':
            searches = load_json_file(searches_json_file())
            for key in sorted(searches.keys()):
                params = searches[key]
                print(f'search name: {key}')

        elif func == 'lookup_doc':
            index_name  = sys.argv[2]
            doc_key     = sys.argv[3]
            client.lookup_doc(index_name, doc_key)

        else:
            print_options('Error: invalid function: {}'.format(func))
            
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
