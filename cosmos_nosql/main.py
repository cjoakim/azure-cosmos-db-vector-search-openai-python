"""
Usage:
  python main.py <func>
  python main.py env
  python main.py load_nosql_baseballplayers
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

from pysrc.nosqlbundle import Bytes, Cosmos, Counter, Env, FS, OpenAIClient, Storage, System

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
    print('AZURE_COSMOSDB_NOSQL_URI:     {}'.format(Env.var('AZURE_COSMOSDB_NOSQL_URI')))
    print('AZURE_COSMOSDB_NOSQL_RW_KEY1: {}'.format(Env.var('AZURE_COSMOSDB_NOSQL_RW_KEY1')))

def wrangled_embeddings_file():
    return '../data/wrangled/documents_with_embeddings.json'

def load_nosql_baseballplayers():
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_NOSQL_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_NOSQL_RW_KEY1')
    c = Cosmos(opts)
    c.set_db('dev')
    c.set_container('baseballplayers')

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
                        result = c.upsert_doc(doc)
                        #print('result: {}'.format(result))
        except Exception as e:
            print(f"Exception on doc: {idx} {doc}")
            print(str(e))
            print(traceback.format_exc())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            func = sys.argv[1].lower()
            if func == 'env':
                check_env()
            elif func == 'load_nosql_baseballplayers':
                load_nosql_baseballplayers()
            else:
                print_options('Error: invalid function: {}'.format(func))
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
    else:
        print_options('Error: no command-line function specified')
