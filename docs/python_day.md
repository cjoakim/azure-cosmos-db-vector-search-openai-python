<p align="center">
    <img src="img/PythonDay.png" width="90%">
</p>

---

## About Chris

- **Career Path**
  - Non-IT --> Software Developer --> Azure Cloud Solution Architect --> **Azure Cosmos DB Global Black Belt (GBB)**
- **Primary Programming Languages Path**
  - COBOL --> Smalltalk --> Java --> Ruby (RoR) --> Node.js (MEAN) --> Java --> **Python**
- **Databases Path**
  - IMS/DB (Hierarchical) --> DB2/Oracle/Sybase/MySQL/PostgreSQL --> **MongoDB (2009) --> Cosmos DB**
- **GitHub**
  - https://github.com/cjoakim
- **PyPi Packages**
  - [m26](https://pypi.org/project/m26/), [ggps](https://pypi.org/project/ggps/), [gdg](https://pypi.org/project/gdg/)

Why show this timeline?
To encourage you to have a [Growth Mindset; and always be learning!](https://www.linkedin.com/pulse/satya-nadella-growth-mindsets-learn-it-all-does-better-jessi-hempel/)

### Why do I use Python now?

- Simple, pragmatic, universally used/understood, great libraries, cross-platform
- **App Dev**: console apps, web apps, Docker, Azure Container Instances, Azure Functions
- **Data Science**: Spark (Synapse), ML/AML/AI... and data wrangling
  - It's currently, IMO, the defacto "Programming Language of Data Science"

---

## This Presentation

- **Vector Search in Microsoft Azure** with:

  - [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
  - [Azure Cosmos DB NoSQL API](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/)
  - [Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/)
  - [The Sean Lahman Baseball Database](http://seanlahman.com/download-baseball-database/) (CSV files)

- **Outline**:

  - [Part 1 - Concepts - Vectors, Vectorization, Vector Search](#part1)
  - [Part 2 - The Business Use-Case](#part2)
  - [Part 3 - Implementation](#part3)

<p align="center">
    <img src="img/architecture.png" width="90%">
</p>

For this **Python Day presentation**, I'll cover the middle solution in the diagram.

---

# <a name="part1"> Part 1 - Concepts

## What is a Vector?

**A Vector is a one-dimensional array of scalar values**.

Think of them as a **numpy array of floats**.

## What is Vectorization?

**Vectorization** is the process of **converting text data into vectors**.

These vectors are called [embeddings](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) in OpenAI.

The [OpenAI SDK](https://platform.openai.com/docs/libraries) contains the functionality
to produce a vector, or an **embedding**, from text data.

OpenAI’s text embeddings measure the **relatedness** of text strings.

Embeddings are dense and are computationally efficient.
They use [Cosine similarity](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/understand-embeddings#cosine-similarity) to measure semantic similarity.

### What does a Vector, or Embedding, look like?

This repo uses **OpenAI embeddings** which are **an array of 1536 floating-point values**
in the range -1 to +1.

It looks very large and verbose, but it's actually **very efficient data structure**
and it enables computational efficiency vs text data.

```
[
    0.002035311423242092,
    -0.0016240125987678766,
    -0.00955343060195446,
    0.019685856997966766,
    -0.037366412580013275,
    0.02373882755637169,
    -0.016621416434645653,
    -0.006778487470000982,
    -0.031858891248703,
    -0.028865059837698936
    ...
    0.01938929781317711,
    -0.007039741612970829,
    0.0302207563072443,
    -0.005779366474598646,
    0.010683178901672363,
    0.00484026363119483,
    0.018556108698248863,
    -0.01864084042608738,
    -0.013634645380079746,
    -0.007526945322751999
]
```

## What is Vector Search?

- Searching a database, or search-engine, using vectors
- A vector is passed in as the **query criteria**
- The DB/engine matches rows/documents **based on the given vector column/attribute in the DB**

### Can I use both standard search and vector search in my Azure Search Engine*?

Yes.  But with different search syntax and parameters.

* = Azure Cognitive Search, Cosmos DB Mongo vCore, Cosmos DB PostgreSQL

### Use-Cases for Vector Search

- Find images that are similar to a given image based on their visual content and style
- Find documents that are similar to a given document based on their topic and sentiment
- Find products that are similar to a given product based on their features and ratings

In short, many use-cases.

But, IMO, it doesn't replace standard search.  It augments it.

---

## What is Azure OpenAI, and why use it here?

> Azure OpenAI Service provides REST API access to OpenAI's powerful language models
> including the GPT-4, GPT-35-Turbo, and Embeddings model series. 
>
> These models can be easily adapted to your specific task including but not limited
> to content generation, summarization, semantic search, and natural language to code
> translation.
>
> Users can access the service through REST APIs, Python SDK, or our
> web-based interface in the Azure OpenAI Studio.

Note: This presentation isn't about the **Generative AI** functionality available in OpenAI.
But **we'll use OpenAI to vectorize our data**.

See [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/).

# <a name="part2"> Part 2 - The Business Use-Case

## What's the Business Problem we're trying to solve?

While other search techniques can answer **simple searches** like:

- Who hits home runs at a similar rate as Hank Aaron?
- Who steals bases at at a similar rate as Rickey Henderson?
- Who has a similar pitching ERA (earned run average) as Ron Guidry?

**This project instead seeks to answer this more complex question, using vector search:**

- **Who has a similar OVERALL PERFORMANCE PROFILE as player x?**

This type of search is more nuanced and subtle, but **can yield more relevant search results**.

--- 

## Example Player: Rickey Henderson

<p align="center">
    <img src="img/rickey-henderson.jpg" width="50%">
</p>

Hall of Fame Player, **Statistical Unicorn** - extremely rare combination of speed
and power.  All-time MLB leader in stolen bases, by far.  Also very high,
statistically, in home runs, triples, walks, IBB, and HBP.

You can try to use a simplistic query (this example is SQL in Azure Cosmos DB PostgreSQL API)
to identify similar players.

<p align="center">
    <img src="img/query-greatest-base-stealers.png" width="95%">
</p>

But this **WHERE clause only contains only three attributes** ... 
it's not a **"full-spectrum" query of the MANY dimensions of baseball player statistics**.

And the results are **sorted by only one column**.

In the vector query search below (bottom of page)
**we'll simply ask instead: find me players like Rickey Henderson!**.

#### But what if you're not in the baseball business?

This vector search app is just an example; it's easily modifiable for your use-cases.

---

# <a name="part3"> Part 3 - Implementation

## Step 1: Data Wrangling

- The data started as CSV files from the [Sean Lahman Baseball Database](http://seanlahman.com/download-baseball-database/)
- CSV rows were transformed into **JSON documents**
- JSON documents augmented with **calculations**
- JSON documents augmented with a **embeddings_str** value for vectorization
- See the [Data Wrangling](data_wrangling.md) page for details

### Example Document for Rickey Henderson

```
  {
    "playerID": "henderi01",
    "birthYear": 1958,
    "birthCountry": "USA",
    "deathYear": "",
    "nameFirst": "Rickey",
    "nameLast": "Henderson",
    "weight": 180,
    "height": 70,
    "bats": "R",
    "throws": "L",
    "debut": "1979-06-24",
    "finalGame": "2003-09-19",
    "teams": {
      "total_games": 3081,
      "teams": {
        "OAK": 1704,
        "NYA": 596,
        "TOR": 44,
        "SDN": 359,
        "ANA": 32,
        "NYN": 152,
        "SEA": 92,
        "BOS": 72,
        "LAN": 30
      },
      "primary_team": "OAK"
    },
    "primary_position": "LF",
    "batting": {
      "G": 3081,
      "AB": 10961,
      "R": 2295,
      "H": 3055,
      "2B": 510,
      "3B": 66,
      "HR": 297,
      "RBI": 1115,
      "SB": 1406,
      "CS": 335,
      "BB": 2190,
      "SO": 1694,
      "IBB": 61,
      "HBP": 98,
      "SF": 67,
      "calculated": {
        "runs_per_ab": 0.20937870632241584,
        "batting_avg": 0.2787154456710154,
        "2b_avg": 0.046528601404981294,
        "3b_avg": 0.006021348417115227,
        "hr_avg": 0.027096067877018522,
        "rbi_avg": 0.10172429522853754,
        "bb_avg": 0.19979928838609615,
        "so_avg": 0.15454794270595748,
        "ibb_avg": 0.005565185658242861,
        "hbp_avg": 0.008940790073898367,
        "sb_pct": 0.8075818495117748
      }
    },
    "category": "fielder",
    "debut_year": 1979,
    "final_year": 2003,
    "embeddings_str": "fielder primary_position_lf total_games_3081 bats_r throws_l hits_3055 hr_297 batting_avg_279 runs_per_ab_209 2b_avg_47 3b_avg_6 hr_avg_27 rbi_avg_102 bb_avg_200 so_avg_155 ibb_avg_6 hbp_avg_9 sb_1406 sb_pct_81",
    "embeddings": [
      -0.028514496982097626,
      0.02490937151014805,
      -0.006417802534997463,
      ...
      -0.01409399788826704,
      -0.026895591989159584,
      -0.007012988440692425
    ]
  }
```

Here's an **embeddings_str text value** in an easier to read format.
**This text value is passed to OpenAI to be "vectorized".**

```
fielder primary_position_lf total_games_3081 bats_r throws_l
hits_3055 hr_297 batting_avg_279 runs_per_ab_209 2b_avg_47 3b_avg_6 
hr_avg_27 rbi_avg_102 bb_avg_200 so_avg_155 ibb_avg_6 hbp_avg_9
sb_1406 sb_pct_81
```

I used the approach of creating **binned-text values** in the embeddings_str.

For example, a batting average of **0.2787154456710154** becomes **"batting_avg_279"**.

A common example of this is **T-shirt sizes** - "S", "M", "L", "XL".

<p align="center">
    <img src="img/tshirt-sizes.png" width="30%">
</p>

See [Binning in Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/group-data-into-bins?view=azureml-api-2)

### Sidebar: Machine Learning "Features" vs Text Words

Since OpenAI embeddings calculation is based on **text**, the binned-text approach is used here.

In Machine Learning, conversely, one instead typically uses **normalized numeric "feature" columns**
in the training dataset.

---

## Step 2: Vectorization

**Vectorization** is the process of converting **text data** into vectors,
which are **one-dimensional arrays of scalar values (floats)**.  

The code required to do this is quite simple, thanks to the **OpenAI SDK** at PyPI.

#### requirements.txt - include the OpenAI SDK library

```
openai
```

#### Python Code

```
from openai.embeddings_utils import get_embedding
from openai.openai_object import OpenAIObject

...

# Configure the openai client library

openai.api_base    = opts['url']   # <-- value from an environment variable, Azure Key Vault, etc
openai.api_key     = opts['key']   # <-- value from an environment variable, Azure Key Vault, etc
openai.api_type    = 'azure'
openai.api_version = '2023-05-15'  # '2022-06-01-preview' '2023-05-15'


# Ask the OpenAI SDK to calculate and return the embedding value.
# The OpenAI embedding model used here is 'text-embedding-ada-002'.

e = openai.Embedding.create(input=[embeddings_str], engine='text-embedding-ada-002')

return e['data'][0]['embedding']  # returns a list of 1536 floats
```

See [Azure OpenAI Service models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models).
These include **GPT-4, GPT-3, text-embedding-ada-002**, etc..

See class OpenAIClient in the repo for the full code; my reusable client module.

---

## Step 3: Loading the Azure Cosmos DB NoSQL API container

It's just a regular Cosmos DB container; no special indexing or attributes are required.
/playerID is the partition key.

#### requirements.txt - include the Cosmos DB NoSQL API SDK library

See [Azure Cosmos DB Python SDK for API for NoSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/sdk-python)
and the [docs](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos?preserve-view=true&view=azure-python).

```
azure-cosmos
```

#### Python Code

```
from azure.cosmos import cosmos_client    <-- client in the Cosmos DB SDK
from azure.cosmos import diagnostics
from azure.cosmos import exceptions

...

class Cosmos():
    """
    This class is used to access a Cosmos DB NoSQL API account.
    """
    def __init__(self, opts):
        self._dbname = None
        self._dbproxy = None
        self._ctrproxy = None
        self._cname = None
        self.reset_record_diagnostics()
        url = opts['url']
        key = opts['key']
        if 'enable_query_metrics' in opts.keys():
            self._query_metrics = True
        else:
            self._query_metrics = False
        self._client = cosmos_client.CosmosClient(url, {'masterKey': key})   <--- create SDK client

...

    # main.py
    # Load the Cosmos DB container with the JSON documents which contain the embeddings array

    def load_nosql_baseballplayers():

        # Connect to Cosmos DB, select database, select container
        opts = dict()
        opts['url'] = Env.var('AZURE_COSMOSDB_NOSQL_URI')
        opts['key'] = Env.var('AZURE_COSMOSDB_NOSQL_RW_KEY1')
        c = Cosmos(opts)
        c.set_db('dev')
        c.set_container('baseballplayers')

        # Read the pre-wrangled documents from a file into a list
        documents = FS.read_json(wrangled_embeddings_file())
        player_ids = sorted(documents.keys())

        # Iterate the list of documents and load Cosmos DB
        for idx, pid in enumerate(player_ids):
            try:
                doc = documents[pid]
                embeddings = doc['embeddings']
                if idx < 100_000:
                    if len(embeddings) == EXPECTED_EMBEDDINGS_ARRAY_LENGTH:  # 1536
                        doc['id'] = str(uuid.uuid4())        <--- create a unique document id
                        result = c.upsert_doc(doc)           <--- insert/update the doc
            except Exception as e:
                print(f"Exception on doc: {idx} {doc}")
                print(traceback.format_exc())
```

See class Cosmos in the repo for the full code; my "DAO" for Cosmos DB NoSQL.
File cosmos_nosql/pysrc/nosqlbundle.py.

---

## Step 4: Configuring Azure Cognitive Search

A full coverage of this is beyond the scope for this brief presentation.

In short, Azure Cognitive Search has a **beautiful and easy to use**
[REST API](https://learn.microsoft.com/en-us/rest/api/searchservice/).

With the REST API these key objects are created - **Datasource**, **Index**, and **Indexer**.
JSON payloads are used to define these objects.

- **Datasource** - defines where the source data is (i.e. - the Cosmos DB account, database, and container)
- **Index** - defines what document attributes to index and make searchable
- **Indexer** - associates a Datasource to an Index, with a schedule

See [Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/)
for more information on these.

See these **JSON schema** files in the repo:
```
cognitive_search/schemas/baseballplayers_index.json
cognitive_search/schemas/baseballplayers_indexer.json
cognitive_search/schemas/datasource-cosmosdb-nosql-dev-baseballplayers.json
```

This repo uses the **Python requests library** to invoke the REST API via HTTPs.

### Sidebar: Why is it called "Cognitive Search"?

In addition to search functionality, **Azure Cognitive Search** offers 
[AI Enrichment](https://learn.microsoft.com/en-us/azure/search/cognitive-search-concept-intro)
functionality, by working with [Azure Cognitive Services](https://azure.microsoft.com/en-ca/products/cognitive-services).

For example, create a document processing **pipeline** to:
- Ingest and "crack" PDF and Word documents
- Extract and identify the images
- Extract the text from the images
- Identify the key words in the text
- Recognize the language and translate the text into another language
- Make the "enriched" content searchable

[Azure Cognitive Services (ACS)](https://learn.microsoft.com/en-us/azure/ai-services/) has a nice 
[Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/cognitive-services?view=azure-python).

Azure Cognitive Services is being renamed to Azure AI Services as it now includes Azure OpenAI.

### Define the embeddings attribute in the Index (see the end of this JSON)

```
{
  "name": "baseballplayers",
  "fields": [
    {
      "name": "id",
      "key": "true",
      "type": "Edm.String",
      "searchable": "true",
      "filterable": "true",
      "sortable": "true",
      "facetable": "true"
    },
    {
      "name": "playerID",
      "key": "false",
      "type": "Edm.String",
      "searchable": "true",
      "filterable": "true",
      "sortable": "true",
      "facetable": "true"
    },
    {
      "name": "birthYear",
      "type": "Edm.Int32",
      "key": "false",
      "searchable": "false",
      "filterable": "true",
      "sortable": "true",
      "facetable": "true"
    },
    {
      "name": "birthCountry",
      "type": "Edm.String",
      "searchable": "true",
      "filterable": "true",
      "sortable": "true",
      "facetable": "true"
    },

    ... 

    {
      "name": "embeddings",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchConfiguration": "vectorConfig"
    }
  ],
  "vectorSearch": {
    "algorithmConfigurations": [
        {
            "name": "vectorConfig",
            "kind": "hnsw"
        }
    ]
  }
}
```

Once the **Indexer** is created, it will read the documents from Cosmos DB to
populate the search Index.

See the [full documentation in this repo](cosmos_nosql_and_cogsearch.md).

---

## Step 5: Executing Vector Searches vs Azure Cognitive Search

### Initial Simple Search

First search the index for the target player (i.e. - Rickey Henderson)
to get their **embeddings value**.

Then use that value for the follow-up vector search.

The HTTP POSTed search request looks like this:
```
{
  "count": "true",
  "search": "playerID eq 'henderi01'",
  "orderby": "playerID",
  "select": "id,playerID,nameFirst,nameLast,primary_position,embeddings_str,embeddings"
}
```

#### Alternative workflow

Given user search criteria, invoke the OpenAI embeddings API with those values
then use the returned embeddings in the follow-up vector search.


### The Vector Search JSON Request looks like this

``` 
{
  "count": "true",
  "select": "id,playerID,nameFirst,nameLast,primary_position",
  "orderby": "playerID",
  "vectors": [
    {
      "value": [
        -0.028514496982097626,
        0.02490937151014805,
        -0.006417802534997463,
        ...
        -0.01409399788826704,
        -0.026895591989159584,
        -0.007012988440692425
      ],
      "fields": "embeddings",
      "k": 10
    }
  ]
}
```

The **value** is the **vector that you want to match**.

**k** is the max number of documents to match.

**embeddings** is the vector attribute in the Index to be matched.

### Search from the command line for players like Rickey Henderson (henderi01)

```
(venv) PS ...\cognitive_search> python cogsearch_main.py vector_search_like baseballplayers henderi01

...

{
  "@odata.context": "https://gbbcjsearch.search.windows.net/indexes('baseballplayers')/$metadata#docs(*)",
  "@odata.count": 10,
  "value": [
    {
      "@search.score": 1.0,
      "id": "e4cc38fd-18c8-4418-8841-98a1403f5ef1",
      "playerID": "bondsba01",
      "nameFirst": "Barry",
      "nameLast": "Bonds",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "c9867b7b-8c34-4e95-a672-16f1bdb393cf",
      "playerID": "brocklo01",
      "nameFirst": "Lou",
      "nameLast": "Brock",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "dff54db9-24c5-42f4-9713-edee804001aa",
      "playerID": "burkeje01",
      "nameFirst": "Jesse",
      "nameLast": "Burkett",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "a12910e7-9542-4c59-a767-4ebb3fddc463",
      "playerID": "henderi01",
      "nameFirst": "Rickey",
      "nameLast": "Henderson",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "949d799f-c8e9-4ee0-a105-91c5f795af18",
      "playerID": "mageesh01",
      "nameFirst": "Sherry",
      "nameLast": "Magee",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "b0c9c139-eec9-4a5a-9d95-1dfa2c80859d",
      "playerID": "meusebo01",
      "nameFirst": "Bob",
      "nameLast": "Meusel",
      "primary_position": "LF"
    },
    {
      "@search.score": 1.0,
      "id": "f1bd535f-f16c-4353-9e2d-338537064404",
      "playerID": "quinnma01",
      "nameFirst": "Mark",
      "nameLast": "Quinn",
      "primary_position": "LF"
    },
```

These search results are more relevant than the simple SQL query as they are
based on **all** of the attributes for the baseball players.

Rickey Henderson, a prolific base stealer as well as power hitter,
thus **matches both Barry Bonds (power hitter) and Lou Brock (base stealer)**.

This search result included only Left-Fielders (**LF**), like Rickey.
The above SQL query result included all positions, which is less relevant.

### Beware of Your Data

Jesse Burkett is in the search results.  He played from 1890-1905.
He stole 389 bases, but was **caught stealing (CS)** zero times - because
that statistic was not kept back then!  Therefore, he appears to
be a prolific and successful base stealer like Rickey Henderson.

Also notice Hugh Duffy in the above SQL query screen-shot; 574 steals, zero times caught!


### Links/References

- https://learn.microsoft.com/en-us/azure/search/vector-search-overview
- https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-query?tabs=portal-vector-query
- File cognitive_search/cogsearch_baseballplayers_searches.ps1 in the repo

---

## Confessions of a Python Developer

### "bundle" modules

You might be asking what are these **xxxbundle.py** modules are in the repo?!

To achieve agile **code reuse** across my many demo repos, I have a standard
core codebase in a private repo.  I develop and test the reusable classes there,
then **bundle** them, with a python script, into function-specific single-file
python modules for use in my implementation repos.  For example **aibundle.py**
and **nosqlbundle.py**.

Since I do about half of my Python programming in **Spark/PySpark**
(in Azure Synapse and Azure Machine Learning) this approach works well for me
because I can simply copy a bundle module into a Spark Notebook cell verbatim.

Yes, alternatively, I could publish a PyPi package for this.

### pylint

I use [pylint](https://pypi.org/project/pylint/) in my core repo.
Sometimes it hurts my feelings, but it's a good impartial code reviewer.

### typings

I just stated to use the [typing](https://docs.python.org/3/library/typing.html)
standard library this year.  I find that it helps me remember the datatypes of
method args and returned values, like this:

```
  def greeting(name: str) -> str:
      return 'Hello ' + name
```

See [Python Enhancement Proposal (PEP) 483](https://peps.python.org/pep-0483/)

### GitHub CoPilot

It's amazing; it reads my mind and saves me a lot of dev time.  "AI pair programmer".

It utilizes the [OpenAI Codex model](https://openai.com/blog/openai-codex).

I use it with both [Visual Studio Code](https://code.visualstudio.com/docs/editor/artificial-intelligence)
and [JetBrains PyCharm](https://docs.github.com/en/copilot/configuring-github-copilot/configuring-github-copilot-in-your-environment?tool=jetbrains).

See https://github.com/features/copilot

---

<p align="center">
    <img src="img/questions-thank-you.png" width="40%">
</p>
