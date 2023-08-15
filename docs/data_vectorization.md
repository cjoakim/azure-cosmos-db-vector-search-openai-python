# Data Vectorization

This GitHub repo contains all of the necessary raw and wrangled (i.e. - prepared) data
files for you to use.  Specifically, it contains file **data/wrangled/documents.json**.

You, however, have to vectorize the **documents.json** data yourself, using
**your Azure OpenAI account** and one of the following two scripts in this repo.

```
data_wrangling/bb_vectorize.ps1
data_wrangling/bb_vectorize.sh
```

## What is Vectorization?

In this context, **vectorization** is the process of converting data into vectors,
which are **one-dimensional arrays of scalar values**.

## What are Embeddings?

Embeddings is another word for a vector.

[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) are
**calculated from an input text value**.  The return value is an array,
or vector, of floating-point numbers.

**Embeddings are used to measure the relatedness of text strings when searched**.

## How are Embeddings used in this Project?

The pre-wrangled data file in this repo, **data/wrangled/documents.json**,
contains approximately 18K Baseball Player documents.  Each Player document
contains a pre-computed value named **embeddings_str**.  Think of the embeddings_str
value as a set of **text-based features** for each player.

This project invokes the **OpenAI API**, passing the **embeddings_str** value
and the model name **text-embedding-ada-002**.  The returned value,
is **an array of 1536 floating-point values**.  See example below.

The Python code to invoke the OpenAI API looks like the following, 
were e is the returned embedding.

```
e = openai.Embedding.create(input=[text], engine='text-embedding-ada-002')
```

```
    "embeddings": [
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

The returned embeddings values are added to the original documents
and then saved to file **data/wrangled/documents_with_embeddings.json**.

This one file - **documents_with_embeddings.json** - is then used to
load all three Cosmos DB databases - Mongo vCore, NoSQL, and PostgreSQL.

Thus, similar baseball players can be vector-searched.

## Execute the Data Vectorization Process

Follow these steps:

```
> cd data_wrangling

> .\venv.ps1                  

> .\venv\Scripts\activate

> mkdir tmp

> .\bb_vectorize.ps1
```

The last script creates file **/data/wrangled/documents_with_embeddings.json**,
which is used to load all three Cosmos DB databases.
Because this JSON file is large, it is "git-ignored" - see the .gitignore file.

The Python implemenentation code in this repo attempts to handle OpenAI
**request throttling** with a **linear backoff** approach so that the
vectorization script will complete successfully.

---

## Next

Proceed to the section for the Cosmos DB database(s) you wish to implement vector search with:

- [Azure Cosmos DB vCore Mongo API searching](cosmos_vcore.md)
- [Azure Cosmos DB NoSQL API with Azure Cognitive Search searching](cosmos_nosql_and_cogsearch.md)
- [Azure Cosmos DB PostgreSQL API with pgvector](cosmos_pg_pgvector.md)
