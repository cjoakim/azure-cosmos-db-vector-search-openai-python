"""
Usage:
  python main.py <func>
  -
  python main.py check_environment_variables
  -
  python main.py psycopg2_example <envname> <dbname>
  python main.py psycopg2_example cosmos citus
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

def psycopg2_example(envname, dbname):
    print('psycopg2_example')
    client = PostgreSqlClient(envname, dbname)
    cursor = client.get_cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS pharmacy;")
    print("Finished dropping table (if existed)")

    # Create a table
    cursor.execute("CREATE TABLE pharmacy (pharmacy_id integer, pharmacy_name text, city text, state text, zip_code integer);")
    print("Finished creating table")

    # Create a index
    cursor.execute("CREATE INDEX idx_pharmacy_id ON pharmacy(pharmacy_id);")
    print("Finished creating index")

    # Insert some data into the table
    cursor.execute("INSERT INTO pharmacy (pharmacy_id,pharmacy_name,city,state,zip_code) VALUES (%s, %s, %s, %s,%s);", (1,"Target","Sunnyvale","CA",94001))
    cursor.execute("INSERT INTO pharmacy (pharmacy_id,pharmacy_name,city,state,zip_code) VALUES (%s, %s, %s, %s,%s);", (2,"CVS","Davidson","NC",28036))
    print("Inserted 2 rows of data")

    client.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options(None)
    else:
        func = sys.argv[1].lower()
        if func == 'check_environment_variables':
            check_environment_variables()
        elif func == 'psycopg2_example':
            envname, dbname = sys.argv[2], sys.argv[3]
            psycopg2_example(envname, dbname)
        else:
            print_options('Error: invalid function: {}'.format(func))
