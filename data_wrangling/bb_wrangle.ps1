# Wrangle the raw baseball CSV files into enhanced JSON documents
# for Azure Cosmos DB and Azure Cognitive Search.
# Chris Joakim, Microsoft, 2023

mkdir .\tmp -Force | Out-Null
del   .\tmp\*.*

echo 'activate venv and display python version:'
.\venv\Scripts\Activate.ps1
python --version

# Prune unnecessary columns from the Lahman Baseball Database CSV files.
python .\bb_wrangle.py prune_people
python .\bb_wrangle.py prune_player_positions
python .\bb_wrangle.py prune_player_teams
python .\bb_wrangle.py prune_batters
python .\bb_wrangle.py prune_pitchers

# Read the pruned CSV files, produce JSON files with calculated attributes.
python .\bb_wrangle.py calc_player_positions
python .\bb_wrangle.py calc_player_teams
python .\bb_wrangle.py calc_batters_stats
python .\bb_wrangle.py calc_pitchers_stats

# Build/assemble the three document types from the joined data.
# The output JSON files are saved in GitHub for end-user/customer processing.
python .\bb_wrangle.py build_documents

python .\bb_wrangle.py scan_documents

echo 'listing of all tmp files:'
dir tmp\*.*

echo 'done'
