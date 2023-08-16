"""
Usage:
  python main.py <func>
  python main.py env
  python main.py load_vcore_baseball_players
  python main.py search_player_like <player_id>
  python main.py search_player_like aaronha01
  python main.py search_player_like jeterde01
  python main.py search_player_like henderi01
  python main.py search_player_like blombro01
  python main.py search_player_like guidrro01
  python main.py search_player_like rosepe01
  python main.py random_player_search
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2023

import base64
import json
import sys
import time
import os
import random
import traceback
import uuid

from docopt import docopt

from pysrc.mongobundle import Bytes, Counter, Env, FS, Mongo, OpenAIClient, Storage, System, Template

import matplotlib
import openai
import pandas as pd
import requests
import tiktoken

from docopt import docopt

from openai.openai_object import OpenAIObject
from openai.embeddings_utils import get_embedding

EXPECTED_EMBEDDINGS_ARRAY_LENGTH = 1536

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def check_env():
    print('AZURE_COSMOSDB_MONGO_VCORE_CONN_STR: {}'.format(Env.var('AZURE_COSMOSDB_MONGO_VCORE_CONN_STR')))

def wrangled_embeddings_file():
    return '../data/wrangled/documents_with_embeddings.json'

def load_vcore_baseball_players():
    opts = dict()
    opts['conn_string'] = Env.var('AZURE_COSMOSDB_MONGO_VCORE_CONN_STR')
    dbname, cname = 'dev', 'baseball_players'
    m = Mongo(opts)
    m.set_db(dbname)
    m.set_coll(cname)
    count = m.count_docs({})
    print('document count in db: {}, collection: {} = {}'.format(dbname, cname, count))
    
    documents = FS.read_json(wrangled_embeddings_file())
    player_ids = sorted(documents.keys())

    for idx, pid in enumerate(player_ids):
        try:
            doc = documents[pid]
            embeddings = doc['embeddings']
            if idx < 100_000:
                if len(embeddings) == EXPECTED_EMBEDDINGS_ARRAY_LENGTH:
                    id = str(uuid.uuid4())
                    print('inserting doc: {} {} {}'.format(idx, id, pid)) 
                    doc['id'] = id 
                    if True:
                        result = m.insert_doc(doc)
                        print('result: {}'.format(result))
        except Exception as e:
            print(f"Exception on doc: {idx} {doc}")
            print(str(e))
            print(traceback.format_exc())

def search_player_like(pid):
    # create the output document:
    outfile = 'tmp/vcore_search_player_like_{}.json'.format(pid)
    output_doc = {}
    output_doc['pid'] = pid
    output_doc['player'] = {}
    output_doc['pipeline'] = pid
    output_doc['results'] = []

    # Connect to the Cosmos DB Mongo vCore account, database, and collection:
    opts = dict()
    opts['conn_string'] = Env.var('AZURE_COSMOSDB_MONGO_VCORE_CONN_STR')
    dbname, cname = 'dev', 'baseball_players'
    m = Mongo(opts)
    m.set_db(dbname)
    m.set_coll(cname)

    print('===')
    print(f'searching for: {pid}')
    player = m.find_one({'playerID': pid})
    if player is None:
        print(f'player not found: {pid}')
        return
    else:
        player['_id'] = str(player['_id'])  # an ObjectId is not JSON serializable, so stringify it
        output_doc['player'] = player
        id    = player['playerID']
        first = player['nameFirst']
        last  = player['nameLast']
        pos   = player['primary_position']
        estr  = player['embeddings_str']
        print('found player: {} {} {} {}'.format(pid, first, last, pos))

    # construct a Mongo aggregation pipeline JSON structure:
    cosmosSearch = dict()
    cosmosSearch['vector'] = player['embeddings']
    cosmosSearch['path'] = 'embeddings'
    cosmosSearch['k'] = 10
    search = dict()
    search['cosmosSearch'] = cosmosSearch
    search['returnStoredSource'] = True
    stage = dict()
    stage['$search'] = search
    pipeline = [stage]
    output_doc['pipeline'] = pipeline
    #print(json.dumps(pipeline, sort_keys=False, indent=2))

    # The aggregation pipeline should look like this:
    # db.exampleCollection.aggregate([
    #   {
    #     "$search": {
    #       "cosmosSearch": {
    #         "vector": [
    #           -0.03235216066241264,
    #           0.016530998051166534,
    #           -0.004801633767783642,
    #           0.01107754372060299,
    #           ...
    #           0.007152967154979706,
    #           -0.005310122389346361,
    #           -0.010333580896258354,
    #           -0.03164232522249222,
    #           -0.006484082899987698
    #         ],
    #         "path": "embeddings",
    #         "k": 10
    #       },
    #       "returnStoredSource": true
    #     }
    #   }
    # ]);

    # execute the aggregation pipeline:
    results = m.aggregate(pipeline)

    # display the search results:
    result_count = 0
    for result_doc in results:
        result_count += 1
        id    = result_doc['playerID']
        first = result_doc['nameFirst']
        last  = result_doc['nameLast']
        pos   = result_doc['primary_position']
        estr  = result_doc['embeddings_str']
        print('result {}: {} {} {} {}'.format(result_count, id, first, last, pos))
        result_doc['_id'] = str(result_doc['_id'])  # an ObjectId is not JSON serializable
        output_doc['results'].append(result_doc)

    # prune the embeddings before writing the output JSON file:
    output_doc['player']['embeddings'] = 'removed'
    for result_doc in output_doc['results']:
        result_doc['embeddings'] = 'removed'
    print('result_count: {}'.format(result_count))
    FS.write_json(output_doc, outfile) 

def random_player_search():
    print('===')
    print('random_player_search...')
    documents = FS.read_json(wrangled_embeddings_file())
    player_ids = sorted(documents.keys())
    random_pid = random.choice(player_ids)
    print('random_pid: {}'.format(random_pid))
    search_player_like(random_pid)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            func = sys.argv[1].lower()
            if func == 'env':
                check_env()
            elif func == 'load_vcore_baseball_players':
                load_vcore_baseball_players()
            elif func == 'random_player_search':
                random_player_search()
            elif func == 'search_player_like':
                pid = sys.argv[2]
                search_player_like(pid)
            else:
                print_options('Error: invalid function: {}'.format(func))
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
    else:
        print_options('Error: no command-line function specified')
