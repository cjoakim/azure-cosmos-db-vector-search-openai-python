"""
Usage:
  python main.py <func>
  -
  python main.py check_environment_variables
  -
  python main.py load_baseball_players <envname> <dbname>
  python main.py load_baseball_players cosmos citus
  -
  python main.py search_similar_baseball_players <envname> <dbname> <player-id>
  python main.py search_similar_baseball_players cosmos citus aaronha01
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import base64
import json
import os
import sys
import time
import traceback

from docopt import docopt

import psycopg2
from psycopg2 import pool

from pysrc.minbundle import Bytes, Counter, Env, FS, Storage, System

EXPECTED_EMBEDDINGS_ARRAY_LENGTH = 1536

class PostgreSqlClient(object):

    def __init__(self, envname, dbname):
        self.envname = envname
        self.dbname  = dbname
        self.pgpool  = None
        self.conn    = None
        self.cursor  = None

        # default to 'localhost'
        host     = "localhost"
        user     = os.environ['USERNAME']
        password = os.environ['LOCAL_PG_PASS']
        sslmode  = ""

        if envname == 'flex':
            host     = os.environ['AZURE_PG_SERVER_FULL_NAME']
            user     = os.environ['AZURE_PG_USER']
            password = os.environ['AZURE_PG_PASS']
            sslmode  = "sslmode=require"
        elif envname == 'cosmos':
            host     = os.environ['AZURE_COSMOSDB_PG_SERVER_FULL_NAME']
            user     = os.environ['AZURE_COSMOSDB_PG_ADMIN_ID']
            password = os.environ['AZURE_COSMOSDB_PG_ADMIN_PW']
            sslmode  = "sslmode=require"

        # Build a connection string from the variables
        self.conn_string = "host={} user={} dbname={} password={} {}".format(
            host, user, dbname, password, sslmode)

        self.pgpool = psycopg2.pool.SimpleConnectionPool(1, 20, self.conn_string)
        if (self.pgpool != None):
            print("Connection pool created")

        # Use getconn() to get a connection from the connection pool
        self.conn = self.pgpool.getconn()
        if (self.conn != None):
            print("Connection created")

    def get_cursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def close(self) -> None:
        """ commit the cursor and close the db connection, if they exist """
        if (self.cursor != None):
            self.cursor.close()
        if (self.conn != None):
            self.conn.commit()
            self.conn.close()
            print("Connection closed")


def print_options(msg=None):
    if msg:
        print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def check_environment_variables():
    home = Env.var('USERNAME')
    env_vars = [
        'USERNAME',
        'LOCAL_PG_PASS',
        'AZURE_PG_SERVER_FULL_NAME',
        'AZURE_PG_USER',
        'AZURE_PG_PASS',
        'AZURE_COSMOSDB_PG_ADMIN_ID',
        'AZURE_COSMOSDB_PG_ADMIN_PW',
        'AZURE_COSMOSDB_PG_SERVER_FULL_NAME'
    ]
    for env_var in env_vars:
        print('check_env, {}: {}'.format(env_var, str(Env.var(env_var))))

def delete_define_players_table(envname, dbname):
    print('TODO - implement delete_define_players_table()')
    client = PostgreSqlClient(envname, dbname)
    cursor = client.get_cursor()
    tablename = 'players_xxx'

    # Drop previous table of same name if one exists
    cursor.execute(f"DROP TABLE IF EXISTS {tablename};")
    print("Finished dropping table (if existed)")

    # Create a table - TODO
    cursor.execute(f"CREATE TABLE {tablename} (pharmacy_id integer, pharmacy_name text, city text, state text, zip_code integer);")
    print("Finished creating table")

    # Create a index
    cursor.execute(f"CREATE INDEX idx_pharmacy_id ON {tablename}(pharmacy_id);")
    print("Finished creating index")
    client.close()

def load_baseball_players(envname, dbname):
    try:
        client = PostgreSqlClient(envname, dbname)
        cursor = client.get_cursor()
        columns_list = [
            'id',
            'player_id',
            'birth_year',
            'birth_country',
            'first_name',
            'last_name',
            'bats',
            'throws',
            'category',
            'primary_position',
            'teams_data',
            'pitching_data',
            'batting_data',
            'embeddings_str',
            'embeddings'
        ]
        columns_tup = str(tuple(columns_list)).replace("'",'')

        print('reading the wrangled_embeddings_file...')
        documents = FS.read_json(wrangled_embeddings_file())
        player_ids = sorted(documents.keys())

        for idx, pid in enumerate(player_ids):
            try:
                doc = documents[pid]
                embeddings = doc['embeddings']
                if idx < 100_000:
                    if len(embeddings) == EXPECTED_EMBEDDINGS_ARRAY_LENGTH:
                        id = idx + 1
                        pid = doc['playerID']
                        print(f'loading {id} {pid}')
                        column_values = []
                        column_values.append(id)
                        column_values.append(doc['playerID'])
                        column_values.append(doc['birthYear'])
                        column_values.append(doc['birthCountry'])
                        column_values.append(str(doc['nameFirst']).replace("'",''))
                        column_values.append(str(doc['nameLast']).replace("'",''))
                        column_values.append(doc['bats'])
                        column_values.append(doc['throws'])
                        column_values.append(doc['category'])
                        column_values.append(doc['primary_position'])
                        teams_data    = json.dumps(get_jsonb_value(doc, 'teams'))
                        pitching_data = json.dumps(get_jsonb_value(doc, 'pitching'))
                        batting_data  = json.dumps(get_jsonb_value(doc, 'batting'))
                        column_values.append(teams_data)
                        column_values.append(pitching_data)
                        column_values.append(batting_data)
                        column_values.append(doc['embeddings_str'])
                        column_values.append(str(doc['embeddings']))
                        values_tup = tuple(column_values)
                        sql_stmt = f'insert into players {columns_tup} values {values_tup};'
                        #print(sql_stmt)
                        cursor.execute(sql_stmt)
                        client.conn.commit()
            except Exception as e:
                print(f"Exception on doc: {idx} {values_tup}")
                print(str(e))
                print(traceback.format_exc())
    except Exception as excp:
        print(str(excp))
        print(traceback.format_exc())

    client.close()

def search_similar_baseball_players(envname, dbname, player_id):
    print(f'search_similar_baseball_players: {envname} {dbname} {player_id}')
    client = None
    try:
        # See https://wiki.postgresql.org/wiki/Psycopg2_Tutorial
        client = PostgreSqlClient(envname, dbname)
        cursor = client.get_cursor()
        sql = f"select player_id, embeddings from players where player_id = '{player_id}'"
        embeddings = None

        cursor.execute(sql)
        rows = cursor.fetchall()
        for row_idx, row in enumerate(rows):
            if row_idx == 0:
                pid, embeddings = row[0], row[1]  # row is a tuple of n-column values per sql

        if embeddings != None:
            sql = vector_query_sql(embeddings)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row_idx, row in enumerate(rows):
                seq = row_idx + 1
                pid = row[0]
                first_name = row[1]
                last_name = row[2]
                position = row[5]
                print(f'result {seq}: {pid} {first_name} {last_name} {position}')

    except Exception as excp:
        print(str(excp))
        print(traceback.format_exc())
    finally:
        if client != None:
            client.close()

def vector_query_sql(embeddings):
    return """
select player_id, first_name, last_name, bats, throws, primary_position, batting_data
from players
order by embeddings <-> '{}'
limit 10;
    """.format(embeddings).strip()

def wrangled_embeddings_file():
    return '../data/wrangled/documents_with_embeddings.json'

def get_jsonb_value(doc, key):
    if key in doc.keys():
        return doc[key]
    else:
        return {}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options(None)
    else:
        func = sys.argv[1].lower()
        if func == 'check_environment_variables':
            check_environment_variables()
        elif func == 'delete_define_players_table':
            envname, dbname = sys.argv[2], sys.argv[3]
            delete_define_players_table(envname, dbname)
        elif func == 'load_baseball_players':
            envname, dbname = sys.argv[2], sys.argv[3]
            load_baseball_players(envname, dbname)
        elif func == 'search_similar_baseball_players':
            envname, dbname, player_id = sys.argv[2], sys.argv[3], sys.argv[4]
            search_similar_baseball_players(envname, dbname, player_id)
        else:
            print_options('Error: invalid function: {}'.format(func))
