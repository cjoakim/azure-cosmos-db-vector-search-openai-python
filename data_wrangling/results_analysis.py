"""
Usage:
  python results_analysis.py collect_results
  python results_analysis.py compare_results
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2023

import json
import os
import sys
import traceback

import pandas as pd

from docopt import docopt

from pysrc.aibundle import Bytes, CogSearchClient, CogSvcsClient, Counter, Env, FS, Mongo, OpenAIClient, Storage, StringUtil, System

PLAYERS_DICT = {}
SEARCH_RESULTS_LIST = []
SEARCH_RESULTS_DICT = {}

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def searched_player_ids():
    return 'aaronha01,blombro01,guidrro01,henderi01,jeterde01,rosepe01'.split(',')

def collect_results():
    collect_cogsearch_results()
    collect_vcore_results()
    collect_pgvector_results()
    collect_embeddings_str_values()

    data = {}
    data['PLAYERS_DICT'] = PLAYERS_DICT
    data['SEARCH_RESULTS_LIST'] = SEARCH_RESULTS_LIST
    data['SEARCH_RESULTS_DICT'] = SEARCH_RESULTS_DICT
    outfile = '../data/search_results/collected_results.json'
    FS.write_json(data, outfile)


def collect_cogsearch_results():
    for pid in searched_player_ids():
        srd_key = f'cogsearch_{pid}'
        SEARCH_RESULTS_DICT[srd_key] = []  
        PLAYERS_DICT[pid] = ''
        infile = f'../data/search_results/cogsearch/search_vector_{pid}.json'
        results = FS.read_json(infile)
        print(f'collect_cogsearch_results: {infile}')
        for result_idx, result in enumerate(results['value']):
            rpid = result['playerID']
            PLAYERS_DICT[rpid] = ''
            SEARCH_RESULTS_LIST.append(['cogsearch', pid, result_idx + 1, rpid])
            SEARCH_RESULTS_DICT[srd_key].append(rpid)

def collect_vcore_results():
    for pid in searched_player_ids():
        srd_key = f'vcore_{pid}'
        SEARCH_RESULTS_DICT[srd_key] = []  
        infile = f'../data/search_results/vcore/vcore_search_player_like_{pid}.json'
        results = FS.read_json(infile)
        print(f'collect_vcore_results: {infile}')
        for result_idx, result in enumerate(results['results']):
            rpid = result['playerID']
            PLAYERS_DICT[rpid] = ''
            SEARCH_RESULTS_LIST.append(['vcore', pid, result_idx + 1, rpid])
            SEARCH_RESULTS_DICT[srd_key].append(rpid)

def collect_pgvector_results():
    for pid in searched_player_ids():
        srd_key = f'pgvector_{pid}'
        SEARCH_RESULTS_DICT[srd_key] = []  
        infile = f'../data/search_results/pgvector/pgvector_search_player_like_{pid}.json'
        results = FS.read_json(infile)
        print(f'collect_pgvector_results: {infile}')
        for result_idx, result in enumerate(results):
            rpid = result['player_id']
            PLAYERS_DICT[rpid] = ''
            SEARCH_RESULTS_LIST.append(['pgvector', pid, result_idx + 1, rpid])
            SEARCH_RESULTS_DICT[srd_key].append(rpid)
            
def collect_embeddings_str_values():
    infile = '../data/wrangled/documents.json'
    documents = FS.read_json(infile)
    for pid in sorted(PLAYERS_DICT.keys()):
        if pid in documents.keys():
            estr = documents[pid]['embeddings_str']
            PLAYERS_DICT[pid] = estr

    
def compare_results():
    pass

def verbose():
    for arg in sys.argv:
        if arg == '--verbose':
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            func = sys.argv[1].lower()
            if func == 'collect_results':
                collect_results()
            elif func == 'compare_results':
                compare_results()
            else:
                print_options('Error: invalid function: {}'.format(func))
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
    else:
        print_options('Error: no command-line function specified')
