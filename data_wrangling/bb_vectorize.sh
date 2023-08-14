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
python bb_wrangle.py add_embeddings_to_documents

python bb_wrangle.py scan_embeddings

python bb_wrangle.py csv_reports

echo 'listing of all tmp files:'
ls -al tmp/*.*

echo 'done'