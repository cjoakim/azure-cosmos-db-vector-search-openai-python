# Azure Cosmos DB NoSQL API with Azure Cognitive Search

## Documentation

Please refer to these Azure documentation pages.

### Azure Cosmos DB vCore API

- https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search

### Azure Cosmos DB NoSQL API with Azure Cognitive Search

- https://learn.microsoft.com/en-us/azure/search/vector-search-overview
- https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-query

---

## Azure Cosmos DB NoSQL API

In the [Azure Provisioning](azure_provisioning.md) section of this project
we created your Cosmos DB NoSQL account and simply created the **dev** database,
with a container named **baseballplayers** which uses **/playerID** as the
partition key.

All we have to do now is load that container as follows:

```
> cd cosmos_nosql

> .\venv.ps1                  

> .\venv\Scripts\activate

> mkdir tmp

> python main.py load_nosql_baseballplayers
```

This **load_nosql_baseballplayers** process will take several minutes to run
depending on your computer and network speed. Over 18,000 documents will be
loaded into the database.

While the Cosmos DB NoSQL API supports SQL-based queries, it doesn't support
search natively.  However, it integrates very easily with **Azure Cognitive Search**.

---

## Azure Cognitive Search

In the [Azure Provisioning](azure_provisioning.md) section of this project
we simply created a **Cognitive Search** account with no additional configuration.

We'll now use the Azure Cognitive Search **REST API** to create a **Datasource**
for your Cosmos DB account, an **Index** that defines the attributes within a Cosmos DB
container to be indexed, and an **Indexer** which periodically reads the
Datasoure to populate the Index.  Once the Index is populated, we can query
it with the REST API.  Python code, using the [requests](https://pypi.org/project/requests/)
library, invokes the REST API via HTTPs.  Credentials are passed as HTTP headers.

### Configuring your Azure Cognitive Search

```
> cd cognitive_search

> .\venv.ps1                  

> .\venv\Scripts\activate

> mkdir tmp

> .\cogsearch_baseballplayers_create.ps1
```

The **cogsearch_baseballplayers_create.ps1** script will first delete indexer,
index, and datasource, then recreate them in the reverse order. 

The output will be simiar to the following:

```
(venv) PS ...\cognitive_search> .\cogsearch_baseballplayers_create.ps1
deleting output tmp/ files ...
============================================================
['cogsearch_main.py', 'display_config']
search_name:      gbbcjsearch
search_url:       https://gbbcjsearch.search.windows.net
search_admin_key: BZ2B... secret ...
search_query_key: bM63... secret ...
admin_headers:
{
  "Content-Type": "application/json",
  "api-key": "BZ2B... secret ..."
}
query_headers:
{
  "Content-Type": "application/json",
  "api-key": "bM63... secret ..."
}
============================================================
['cogsearch_main.py', 'delete_indexer', 'baseballplayers']
============================================================
['cogsearch_main.py', 'delete_index', 'baseballplayers']
============================================================
['cogsearch_main.py', 'delete_datasource', 'cosmosdb-nosql-dev-baseballplayers']
============================================================
['cogsearch_main.py', 'create_cosmos_nosql_datasource', 'AZURE_COSMOSDB_NOSQL_ACCT', 'AZURE_COSMOSDB_NOSQL_RO_KEY1', 'dev', 'baseballplayers']
file written: tmp/create_cosmos_nosql_datasource_dev_baseballplayers_1691615622.json
============================================================
['cogsearch_main.py', 'create_index', 'baseballplayers', 'baseballplayers_index.json']
file written: tmp/create_index_baseballplayers_1691615636.json
============================================================
['cogsearch_main.py', 'create_indexer', 'baseballplayers', 'baseballplayers_indexer.json']
file written: tmp/create_indexer_baseballplayers_1691615645.json
============================================================
['cogsearch_main.py', 'get_indexer_status', 'baseballplayers']
file written: tmp/get_indexer_status_1691615652.json
============================================================
['cogsearch_main.py', 'list_datasources']
file written: tmp/list_datasources_1691615659.json
============================================================
['cogsearch_main.py', 'list_indexes']
file written: tmp/list_indexes_1691615666.json
============================================================
['cogsearch_main.py', 'list_indexers']
file written: tmp/list_indexers_1691615673.json
done
```

You can look at the output files in the tmp/ directory to see the
results of each operation.  For example, file 
"tmp/create_indexer_baseballplayers_1691615645.json".
In this example 1691615645 is the execution epoch timestamp.

### Azure Portal

You can go to your Azure Cognitive Search account in Azure Portal to
**confirm that the **Datasource, Index, and Indexer** have been created.**
The following screen-shots show these.  These screen shots also some
airports and routes objects but these aren't part of this project.
The **baseballplayers** objects pertain to this project.

<p align="center">
    <img src="img/cog-search-datasources.png" width="80%">
</p>

---

<p align="center">
    <img src="img/cog-search-indexes.png" width="80%">
</p>

---

<p align="center">
    <img src="img/cog-search-indexers.png" width="80%">
</p>

Per this screen shot, the Indexer ran successfully and indexed all 18,221
documents in the Cosmos DB container.  On subsequent runs of the Indexer,
however, zero or few documents may be indexed because Azure Cognitive Search
only indexes the documents that have changed since the last run of the Indexer.

The **Indexer** used in this project is defined with this JSON document.
The **schedule** is defined to run every hour (PT1H) in this example.

```
{
  "name": "baseballplayers",
  "dataSourceName": "cosmosdb-nosql-dev-baseballplayers",
  "targetIndexName": "baseballplayers",
  "schedule": {
    "interval": "PT1H"
  }
}
```

### How Search is Implemented in this Project

The same approach is used here as in the Cosmos DB vCore and PostgreSQL API
apps in this project.  First, a lookup search (not a vector search) is
used to lookup the given playerID in the Index.  Then, if the lookup was
successful, the **embeddings** value of that search result are used
to execute a vector search for players similar to those embeddings.

### Executing Searches

Script **cogsearch_baseballplayers_searches.ps1** will execute 
vector searches for players like these players:

```
python cogsearch_main.py search_index baseballplayers aaronha01

python cogsearch_main.py vector_search_like baseballplayers aaronha01
python cogsearch_main.py vector_search_like baseballplayers jeterde01
python cogsearch_main.py vector_search_like baseballplayers henderi01
python cogsearch_main.py vector_search_like baseballplayers blombro01
python cogsearch_main.py vector_search_like baseballplayers guidrro01
python cogsearch_main.py vector_search_like baseballplayers rosepe01
```

#### Sample Output

Here's the output for just Hank Aaron (aaronha01).
The response data from Azure Cognitive Search is in JSON format.

```
['cogsearch_main.py', 'vector_search_like', 'baseballplayers', 'aaronha01']
file written: tmp/search_lookup_aaronha01.json
lookup search successful for player: aaronha01
{
  "count": "true",
  "select": "id,playerID,nameFirst,nameLast,primary_position",
  "orderby": "playerID",
  "vectors": [
    {
      "value": [
        -0.03235216,
        0.016530998,
        -0.004801634,

        ...
        
        -0.010333581,
        -0.031642325,
        -0.006484083
      ],
      "fields": "embeddings",
      "k": 10
    }
  ]
}
file written: tmp/search_vector_aaronha01.json
{
  "@odata.context": "https://gbbcjsearch.search.windows.net/indexes('baseballplayers')/$metadata#docs(*)",
  "@odata.count": 10,
  "value": [
    {
      "@search.score": 1.0,
      "id": "98a97855-b773-4c23-bc3a-3db353990429",
      "playerID": "aaronha01",
      "nameFirst": "Hank",
      "nameLast": "Aaron",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "53a22a8a-5f69-42fc-a9bf-1b6849bcce13",
      "playerID": "chambwe01",
      "nameFirst": "Wes",
      "nameLast": "Chamberlain",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "ecbd8806-7396-4b6b-8709-c208079848d9",
      "playerID": "dawsoan01",
      "nameFirst": "Andre",
      "nameLast": "Dawson",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "e525a44a-6270-4bd1-9fd1-bb5dd07d71c3",
      "playerID": "garciad02",
      "nameFirst": "Adolis",
      "nameLast": "Garcia",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "0097cbc5-7450-495f-8e3b-3f81e75e6675",
      "playerID": "guerrvl01",
      "nameFirst": "Vladimir",
      "nameLast": "Guerrero",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "9017f888-1828-445c-aedb-90ba585ba371",
      "playerID": "kalinal01",
      "nameFirst": "Al",
      "nameLast": "Kaline",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "3b6e988b-455d-4316-a410-48cd4f2020ec",
      "playerID": "ottme01",
      "nameFirst": "Mel",
      "nameLast": "Ott",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "d8efef35-6b61-4168-9590-0709b5d3df4e",
      "playerID": "robinfr02",
      "nameFirst": "Frank",
      "nameLast": "Robinson",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "aa939301-1cfa-4264-a799-9e59b31ee3ab",
      "playerID": "rominke01",
      "nameFirst": "Kevin",
      "nameLast": "Romine",
      "primary_position": "RF"
    },
    {
      "@search.score": 1.0,
      "id": "4f0336f3-f394-4de2-a68b-0f4530e15245",
      "playerID": "sheffga01",
      "nameFirst": "Gary",
      "nameLast": "Sheffield",
      "primary_position": "RF"
    }
  ]
}
```

---

## Summary

- We didn't have to create verbose explicit queries with many attributes, and value ranges for these attributes
- We simply asked Azure Cognitive Search to "find me players like Hank Aaron"
- And the results are very accurate
