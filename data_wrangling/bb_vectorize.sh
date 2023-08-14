#!/bin/bash

# Vectorize the wrangled documents using Azure OpenAI.
# Chris Joakim, Microsoft, 2023

mkdir -p tmp/

echo 'activate venv and display python version:'
source venv/bin/activate
python --version

# Users/Customers generate the embeddings with their own Azure OpenAI account
# per the AZURE_OPENAI_URL and AZURE_OPENAI_KEY1 environment variables.
# The output data file from this step is NOT stored in GitHub.

# The arg '1900' is the minimum debut_year of the player.
# Using a more recent debut_year value will reduce the number
# of rows/documents to be vectorized, and loaded into the DB.

python bb_wrangle.py add_embeddings_to_documents 1900

echo 'listing of all tmp files:'
ls -al tmp/*.*

echo 'done'