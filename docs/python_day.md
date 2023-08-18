# Python Day Presentation

This page summarizes this repo as a **TL;DR**, or short presentation.

---

## About Chris Joakim

- Role
  - **Microsoft Cosmos DB Global Black Belt (GBB)**
- Location
  - Charlotte, NC, USA
- Career Path
  - Non-IT --> Software Developer --> Azure Cloud Solution Architect --> GBB
- Primary Languages
  - COBOL --> Smalltalk --> Java --> Ruby (RoR) --> Node.js (MEAN) --> Java --> **Python**
- Secondary Languages
  - Perl, Awk/Sed, Flex, Clojure, CoffeeScript, TypeScript, C#
- GitHub
  - https://github.com/cjoakim
  - https://github.com/cjoakim/azure-cosmos-db-vector-search-openai-python (this repo)
  - https://github.com/cjoakim/azure-cosmos-db-vector-search-openai-python/blob/main/docs/python_day.md (this presentation)
- [PyPi Packages - m26, ggps, gdg](https://pypi.org/user/cjoakim/)

### Why Python now?

- Simplicity, pragmatic, universally used/understood, and wide range of use-cases
  - console apps, web apps, Docker, Spark (Synapse), ML/AML/AI, Azure Functions
  - Currently the defacto "Programming Language of Data Science" (IMO)

---

## This Presentation

- **Vector Search in Microsoft Azure** with:
  - [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
  - [Azure Cosmos DB NoSQL API](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/)
  - [Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/)
  - The [Sean Lahman Baseball Database](http://seanlahman.com/download-baseball-database/) CSV files

#### Also in this Repo but not covered in this presentation

  - Azure PaaS Service Provisioning
  - Workstation Setup
  - Baseball Database CSV file "data wrangling" process
  - Vector Search with [Azure Cosmos DB Mongo vCore API](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/)
  - Vector Search with [Azure Cosmos DB PostgreSQL API](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/)
  - See the [README](README.md) where these topics are covered

### Also not covered in this presentation

  - The basics of [NoSQL](https://en.wikipedia.org/wiki/NoSQL) and [Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db)

---

## What is Vector Search?


---

## What is Azure OpenAI, and why use it here?


---

## What's the Business Problem we're trying to solve?

While other search techniques can answer **simple searches** like:

- Who hits home runs at a similar rate as Hank Aaron?
- Who steals bases at at a similar rate as Rickey Henderson?
- Who has a similar pitching ERA (earned run average) as Ron Guidry?

**This project instead seeks to answer this more complex question, using vector search:**

- **Who has a similar OVERALL PERFORMANCE PROFILE as player x?**

<p align="center">
    <img src="img/rickey-henderson.jpg" width="40%">
</p>
<p align="center">
    Rickey Henderson (henderi01), MLB Hall of Fame Player, Statistical Unicorn
</p>
<p align="center">
    <img src="img/query-greatest-base-stealers.png" width="80%">
</p>

#### But what if you're not in the baseball business?

This vector search solution is just an example, it's easily modifiable for your use-cases.

---

## Step 1: Data Wrangling

- The data started as CSV from the Sean Lahman Baseball Database
- CSV rows were transformed into JSON documents
- JSON documents augmented with calculations
- JSON documents augmented with a **embeddings_str** value for vectorization

### Example Document for Hank Aaron 

```
  "aaronha01": {
    "playerID": "aaronha01",
    "birthYear": 1934,
    "birthCountry": "USA",
    "deathYear": "2021.0",
    "nameFirst": "Hank",
    "nameLast": "Aaron",
    "weight": 180,
    "height": 72,
    "bats": "R",
    "throws": "R",
    "debut": "1954-04-13",
    "finalGame": "1976-10-03",
    "teams": {
      "total_games": 3298,
      "teams": {
        "ML1": 1806,
        "ATL": 1270,
        "ML4": 222
      },
      "primary_team": "ML1"
    },
    "primary_position": "RF",
    "batting": {
      "G": "3298",
      "AB": "12364",
      "R": "2174",
      "H": "3771",
      "2B": "624",
      "3B": "98",
      "HR": "755",
      "RBI": "2297.0",
      "SB": "240.0",
      "CS": "73.0",
      "BB": "1402",
      "SO": "1383.0",
      "IBB": "293.0",
      "HBP": "32.0",
      "SF": "121.0",
      "calculated": {
        "runs_per_ab": 0.17583306373341961,
        "batting_avg": 0.30499838240051763,
        "2b_avg": 0.050469103849886766,
        "3b_avg": 0.007926237463604012,
        "hr_avg": 0.06106438045939825,
        "rbi_avg": 0.18578130054998382,
        "bb_avg": 0.11339372371400841,
        "so_avg": 0.11185700420575866,
        "ibb_avg": 0.023697832416693626,
        "hbp_avg": 0.002588159171789065
      }
    },
    "category": "fielder",
    "debut_year": 1954,
    "final_year": 1976,
    "embeddings_str": "fielder primary_position_rf total_games_3298 bats_r throws_r hits_3771 hr_755 batting_avg_305 runs_per_ab_176 2b_avg_50 3b_avg_8 hr_avg_61 rbi_avg_186 bb_avg_113 so_avg_112 ibb_avg_24 hbp_avg_3"
  }
```

I used the approach of creating **binned-text** values in the embeddings_str.
For example batting average of 0.30499838240051763 becomes "batting_avg_305".

A common example of this is T-shirt sizes - "S", "M", "L", "XL".

### Machine Learning "Features" vs Text Words

Since OpenAI embeddings calculation is based on **text**, the binned-text approach is used.

---

## Step 2: Vectorization


---

## Step 3: Loading the Azure Cosmos DB NoSQL API container


---

## Step 4: Configuring Azure Cognitive Search

---

## Step 5: Excuting Vector Searches vs Azure Cognitive Search



