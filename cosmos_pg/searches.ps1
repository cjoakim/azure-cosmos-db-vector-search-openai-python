# Execute several vector searches vs Cosmos DB PostgreSQL.
# Chris Joakim, Microsoft, 2023

New-Item -ItemType Directory -Force -Path .\tmp | out-null

del tmp\*search*.json

python main.py search_similar_baseball_players cosmos citus aaronha01

python main.py search_similar_baseball_players cosmos citus jeterde01

python main.py search_similar_baseball_players cosmos citus henderi01

python main.py search_similar_baseball_players cosmos citus blombro01

python main.py search_similar_baseball_players cosmos citus guidrro01

python main.py search_similar_baseball_players cosmos citus rosepe01

echo 'done'
