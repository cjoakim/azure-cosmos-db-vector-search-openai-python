# Azure Provisioning

While Azure resources can be provisioned in an automated manner in several ways
(i.e. - PowerShell, Bicep, the Azure CLI, etc.) the approach taken in this
project is to simply use [Azure Portal](https://portal.azure.com) to
**manually create these resources**.  For new Azure users, this may be the
more educational way to provision Azure resources.

These instructions are intended to be a general guide, rather than a click-by-click
set of instructions.  For full details and instructions, see the pertinent
Azure documentation provided as a hyperlink in each section.

This page describes provisioning these resources used in this project:

- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure Cosmos DB for MongoDB vCore API](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/)
- [Azure Cosmos DB for NoSQL API](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/)
- [Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/)
- [Azure Cosmos DB for PostgreSQL API](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/)

---

## Azure OpenAI

To use this project you **must** have access to an **Azure OpenAI** account.

To create one go to **Marketplace** in Azure Portal and search for "openai"
as shown below.  Then follow the web page dialog to create your account.

<p align="center">
    <img src="img/marketplace-openai.png" width="25%">
</p>

### Add Model Deployments in Azure AI Studio

You'll need to register a **deployment** named **text-embedding-ada-002** that uses an
OpenAI model named **text-embedding-ada-002**.  This deployment will be
used to vectorize the data before you load it into your Cosmos DB database(s).

Click **Model Deployments** in your Azure OpenAI account, this will open
**Azure AI Studio** as shown below.  For simplicity, one naming convention
is to name the deployment the same as the model.  Click "+ Create new deployment"
and proceed with the web dialog.  The following screen-shot shows several
model deployments in this OpenAI account, including "text-embedding-ada-002".

<p align="center">
    <img src="img/azure-openai-model-deployments.png" width="70%">
</p>

### Configuration, Secrets, Environment Variables

In Azure Portal, go to your OpenAI account, then click "Keys and Endpoint"
under Resource Management as shown below:

<p align="center">
    <img src="img/open-ai-keys-endpoint.png" width="70%">
</p>

The code in this project assumes the presence of these several **specific environment variables**,
all described on this page.  For Azure OpenAI, the following two environment variables 
are required.

```
AZURE_OPENAI_URL
AZURE_OPENAI_KEY1
```

Capture their values from Azure Portal, and set them as environment variables
on your workstation/laptop.

For example, **AZURE_OPENAI_URL** should be set to "https://gbbcjopenai.openai.azure.com/"
per the above screen-shot.

In Windows PowerShell, one way to set this environment variable is to run the following command.
Then close and restart PowerShell.

```
> [Environment]::SetEnvironmentVariable("AZURE_OPENAI_URL", "<your-url>", "User")
```

**Please get familiar with this process of setting specific environment variables per your Azure PaaS service, as this process is used for all Azure services used in this project.**

All environment variables described in this page are the required names for
**this project only**; they are not required by Microsoft or OpenAI.

It is assumed here that macOS and Linux users are familiar with setting their
environment variables, such as in file ~/.bash_profile.

### Further Reading

See the [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) documentation.

---

## Azure Cosmos DB for MongoDB vCore API

Go to **Marketplace** in Azure Portal and search for "Cosmos DB".
Select "Azure Cosmos DB" from the seach result, and click "Create".
At the following page, select "Azure Cosmos DB for MongoDB".

<p align="center">
    <img src="img/azure-portal-provision-cosmosdb.png" width="80%">
</p>

Then, at the following page, click "Create" under **vCore cluster**.
Click through the remaining pages of the web-dialog.
For the **Cluster Tier**, a minimal size cluster is necessary for this project.
Be sure to save the username and password you configure.

We'll configure your vCore account later in this project.  We'll add
a database, a container, and an index.

### Configuration, Secrets, Environment Variables

In Azure Portal, go to your vCore account, then click "Connection Strings"
under Settings.

Set environment variable **AZURE_COSMOSDB_MONGO_VCORE_CONN_STR**
to the pattern indicated in Azure Portal. Change the values of
"user", "password", and "your-account" per your account configuration.
Remove the < and > characters.

```
mongodb+srv://<user>:<password>@<your-account>.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000
```

For example, the value of AZURE_COSMOSDB_MONGO_VCORE_CONN_STR should look like:

```
mongodb+srv://chris:secret123@gbbchris.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000
```

### Further Reading

See the [Azure Cosmos DB for MongoDB vCore](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/) documentation.

---

## Azure Cosmos DB NoSQL API

The process of creating a Cosmos DB NoSQL API account is very similar to the
above vCore instructions, but instead select "Azure Cosmos DB NoSQL" and create
a provisioned account, not Serverless.

Once the account is created, create a database named **dev**.  Within this database,
create a container called **baseballplayers** with **/playerID** as the partition key.
4000 Request Units (RU), Autoscale, will be adequate for this project.

### Configuration, Secrets, Environment Variables

In Azure Portal, go to your NoSQL account, then click "Keys" under Settings,
and set the following specific environment variables on your computer
as described above.

```
AZURE_COSMOSDB_NOSQL_ACCT
AZURE_COSMOSDB_NOSQL_RO_KEY1    <-- a read-only key
AZURE_COSMOSDB_NOSQL_RW_KEY1    <-- a read-write key
```

AZURE_COSMOSDB_NOSQL_ACCT should have a simple value like "gbbchris", it is not a URL.

### Further Reading

See the [Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/) documentation.

---

## Azure Cognitive Search

Go to **Marketplace** in Azure Portal and search for "azure cognitive search"
as shown below.  Click "Create" and proceed with the web dialog to create
your account.

That's all the configuration you need to do in Azure Portal for Azure Cognitive Search.
The necessary **DataSource, Index, and Indexer** will be created using the very nice
**REST API**, with a **Python client**, elsewhere in this project.

<p align="center">
    <img src="img/azure-portal-provision-cog-search.png" width="50%">
</p>

Note that there is a similarly named PaaS service called 
**Azure Cognitive Services**, but that service is **not** used in this project.
[Azure Cognitive Services](https://azure.microsoft.com/en-in/products/cognitive-services/)
may potentially be part of your solution for vector search as it offers excellent
text-extraction functionality.

The [azure-cognitive-examples](https://github.com/cjoakim/azure-cognitive-examples)
repo provides some examples of using Azure Cognitive Search.

### Configuration, Secrets, Environment Variables

In Azure Portal, go to your Azure Cognitive Search account, then click "Keys" under Settings,
and set the following specific environment variables on your computer
as described above.

```
AZURE_SEARCH_NAME
AZURE_SEARCH_URL
AZURE_SEARCH_ADMIN_KEY
AZURE_SEARCH_QUERY_KEY
```

For example, actual values look like this:

```
AZURE_SEARCH_NAME       -> gbbcjsearch
AZURE_SEARCH_ADMIN_KEY  -> BZ2...
AZURE_SEARCH_QUERY_KEY  -> bM63...
AZURE_SEARCH_URL        -> https://gbbcjsearch.search.windows.net
```

### Further Reading

See the [Azure Cognitive Search](https://learn.microsoft.com/en-us/azure/search/) documentation.

---

## Azure Cosmos DB PostgreSQL API

Go to **Marketplace** in Azure Portal and search for "Cosmos DB".
Select "Azure Cosmos DB" from the seach result, and click "Create".
At the following page, select "Azure Cosmos DB for PostgreSQL".

Click "Create" and proceed with the web dialog to create
your account.  Select the latest version of PostgreSQL, currently 15.
A minimally sized cluster will be adequate for this project.

<p align="center">
    <img src="img/azure-portal-provision-cosmosdb.png" width="80%">
</p>

### Configuration, Secrets, Environment Variables

<p align="center">
    <img src="img/azure-portal-cosmosdb-pg-conn-strings.png" width="80%">
</p>

Set the following specific environment variables on your computer
using the process described above.

```
AZURE_COSMOSDB_PG_SERVER_FULL_NAME
AZURE_COSMOSDB_PG_ADMIN_ID
AZURE_COSMOSDB_PG_ADMIN_PW
```

For example, actual values look like this:

```
AZURE_COSMOSDB_PG_SERVER_FULL_NAME  -> c-gbbcjcpg.xxxxxxxxxxxxxx.postgres.cosmos.azure.com
AZURE_COSMOSDB_PG_ADMIN_ID          -> citus
AZURE_COSMOSDB_PG_ADMIN_PW          -> <secret!>
```

### Further Reading

See the [Azure Cosmos DB for PostgreSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/) documentation.

---

## Next

[Workstation Setup](workstation_setup.md)
