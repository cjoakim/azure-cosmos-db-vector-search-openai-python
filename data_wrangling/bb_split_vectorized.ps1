# Chris Joakim, Microsoft, 2023

del ..\data\wrangled\players\*.*

python bb_wrangle.py split_vectorized_documents 1950 600

echo 'done'
