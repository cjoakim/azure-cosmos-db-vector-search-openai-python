"""
Usage:
  python results_analysis.py gather_results
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

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def gather_results():
    pass

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
            if func == 'gather_results':
                gather_results()
            elif func == 'compare_results':
                compare_results()
            else:
                print_options('Error: invalid function: {}'.format(func))
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
    else:
        print_options('Error: no command-line function specified')
