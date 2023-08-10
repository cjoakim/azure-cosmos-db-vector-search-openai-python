-- baseball_deldef.sql
-- delete and define Cosmos DB PostgreSQL API tables for this app
-- Chris Joakim, Microsoft 

DROP TABLE IF EXISTS players CASCADE;

create table players (
  id                   bigserial primary key,
  player_id            VARCHAR(32),
  birth_year           INTEGER,
  birth_country        VARCHAR(32),
  first_name           VARCHAR(32),
  last_name            VARCHAR(32),
  bats                 CHAR(1),
  throws               CHAR(1),
  category             VARCHAR(16),
  primary_position     VARCHAR(2),
  teams_data           jsonb,
  pitching_data        jsonb,
  batting_data         jsonb,
  embeddings_str       VARCHAR(255),
  embeddings           vector(1536)
);

\d players
