-- extensions.sql
-- query the installed PostgreSQL extensions
-- Chris Joakim, Microsoft 

-- SELECT CREATE_EXTENSION('vector');  <-- enables pgvector

select * FROM pg_extension order by extname;
