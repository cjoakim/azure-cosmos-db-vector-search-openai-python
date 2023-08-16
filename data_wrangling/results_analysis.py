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

# def search_types():
#     return 'cogsearch,vcore,pgvector'.split(',')

def collected_results_file():
    return '../data/search_results/collected_results.json'

def collect_results():
    collect_cogsearch_results()
    collect_vcore_results()
    collect_pgvector_results()
    collect_embeddings_str_values()
    data = {}
    data['PLAYERS_DICT'] = PLAYERS_DICT
    data['SEARCH_RESULTS_LIST'] = SEARCH_RESULTS_LIST
    data['SEARCH_RESULTS_DICT'] = SEARCH_RESULTS_DICT
    FS.write_json(data, collected_results_file())

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
    data = FS.read_json(collected_results_file())
    PLAYERS_DICT = data['PLAYERS_DICT']
    SEARCH_RESULTS_LIST = data['SEARCH_RESULTS_LIST']
    SEARCH_RESULTS_DICT = data['SEARCH_RESULTS_DICT']

    # Create a CSV file with columns to compare the results side-by-side
    csv_rows = []
    csv_rows.append('...csv header row')
    for pid in sorted(searched_player_ids()):
        c = Counter()
        pid_estr = PLAYERS_DICT[pid]
        cogsearch_pid_list = SEARCH_RESULTS_DICT[f'cogsearch_{pid}']
        vcore_pid_list     = SEARCH_RESULTS_DICT[f'vcore_{pid}']
        pgvector_pid_list  = SEARCH_RESULTS_DICT[f'pgvector_{pid}']

        if array_lengths_are_equal(cogsearch_pid_list, vcore_pid_list, pgvector_pid_list):
            increment_counter(c, cogsearch_pid_list, vcore_pid_list, pgvector_pid_list)
            if debug():
                print('cogsearch_pid_list: {} {}'.format(len(cogsearch_pid_list), cogsearch_pid_list))
                print('vcore_pid_list:     {} {}'.format(len(vcore_pid_list), vcore_pid_list))
                print('pgvector_pid_list:  {} {}'.format(len(pgvector_pid_list), pgvector_pid_list))

            for n in range(len(cogsearch_pid_list)):
                # Build the rows for the side-by-side comparison of player pid.
                row_values = []
                row_values.append(pid)
                row_values.append(str(n + 1))
                # Cogsearch cols
                row_values.append(cogsearch_pid_list[n])
                row_values.append(str(c.get_value(cogsearch_pid_list[n])))
                row_values.append(str(levenshtein_distance(pid, cogsearch_pid_list[n])))

                # vCore cols
                row_values.append(vcore_pid_list[n])
                row_values.append(str(c.get_value(vcore_pid_list[n])))
                row_values.append(str(levenshtein_distance(pid, vcore_pid_list[n])))

                # pgvector cols
                row_values.append(pgvector_pid_list[n])
                row_values.append(str(c.get_value(pgvector_pid_list[n])))
                row_values.append(str(levenshtein_distance(pid, pgvector_pid_list[n])))

                print(','.join(row_values))

        else:
            print('search result pid lists are not the same length')

def array_lengths_are_equal(list1, list2, list3):
    if len(list1) == len(list2):
        if len(list1) == len(list3):
            return True
    return False

def increment_counter(c, pid_list1, pid_list2, pid_list3):
    for pid in pid_list1:
        c.increment(pid)
    for pid in pid_list2:
        c.increment(pid)
    for pid in pid_list3:
        c.increment(pid)

def levenshtein_distance(pid1: str, pid2: str) -> int:
    try:
        estr1_tokens = PLAYERS_DICT[pid1].strip().split(' ')
        estr2_tokens = PLAYERS_DICT[pid2].strip().split(' ')
        sum_dist = 0
        if debug():
            print('levenshtein_distance, estr1_tokens: {}'.format(estr1_tokens))
            print('levenshtein_distance, estr2_tokens: {}'.format(estr2_tokens))
        for idx, token1 in enumerate(estr1_tokens):
            token2 = estr2_tokens[idx]
            dist = StringUtil.levenshtein_distance(token1.strip(), token2.strip())
            sum_dist += dist
        return sum_dist
    except Exception as e:
        print(f"Exception on batter: {pid1} {pid2}")
        print(traceback.format_exc())
        return -1

def debug():
    for arg in sys.argv:
        if arg == '--debug':
            return True
    return False

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
