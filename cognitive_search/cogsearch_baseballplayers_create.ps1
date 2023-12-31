# Delete and recreate the baseballplayers indexing.
#
# Note: delete in the sequence of indexer, index, datasource
# but recreate in the opposite sequence of datasource, index, indexer
#
# Chris Joakim, Microsoft

Write-Output 'deleting output tmp/ files ...'
New-Item -ItemType Directory -Force -Path .\tmp | out-null
del tmp\*.*

Write-Output '============================================================'
python cogsearch_main.py display_config

Write-Output '============================================================'
python cogsearch_main.py delete_indexer baseballplayers
sleep 5

Write-Output '============================================================'
python cogsearch_main.py delete_index baseballplayers
sleep 5

Write-Output '============================================================'
python cogsearch_main.py delete_datasource cosmosdb-nosql-dev-baseballplayers
sleep 30

Write-Output '============================================================'
python cogsearch_main.py create_cosmos_nosql_datasource AZURE_COSMOSDB_NOSQL_ACCT AZURE_COSMOSDB_NOSQL_RO_KEY1 dev baseballplayers
sleep 10

Write-Output '============================================================'
python cogsearch_main.py create_index baseballplayers baseballplayers_index.json
sleep 5

Write-Output '============================================================'
python cogsearch_main.py create_indexer baseballplayers baseballplayers_indexer.json
sleep 5

Write-Output '============================================================'
python cogsearch_main.py get_indexer_status baseballplayers
sleep 5

Write-Output '============================================================'
python cogsearch_main.py list_datasources
sleep 5

Write-Output '============================================================'
python cogsearch_main.py list_indexes
sleep 5

Write-Output '============================================================'
python cogsearch_main.py list_indexers

echo 'done'
