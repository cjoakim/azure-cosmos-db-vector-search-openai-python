# Execute several vector searches vs Cosmos DB Mongo vCore,
# of known player IDs as well as random IDs.
# Chris Joakim, Microsoft, 2023

New-Item -ItemType Directory -Force -Path .\tmp | out-null

del tmp\search*.json

python main.py search_player_like aaronha01

python main.py search_player_like jeterde01

python main.py search_player_like henderi01

python main.py search_player_like blombro01

python main.py search_player_like guidrro01

python main.py search_player_like rosepe01

python main.py random_player_search

echo 'done'
