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
  primary_team         VARCHAR(8),
  debut_year           INTEGER,
  final_year           INTEGER,
  total_games          INTEGER,
  teams_data           jsonb,
  pitching_data        jsonb,
  batting_data         jsonb,
  embeddings_str       VARCHAR(255),
  embeddings           vector(1536)
);

create table batters (
  id                   bigserial primary key,
  player_id            VARCHAR(32),
  birth_year           INTEGER,
  birth_country        VARCHAR(32),
  first_name           VARCHAR(32),
  last_name            VARCHAR(32),
  bats                 CHAR(1),
  throws               CHAR(1),
  primary_position     VARCHAR(2),
  primary_team         VARCHAR(8),
  debut_year           INTEGER,
  final_year           INTEGER,
  total_games          INTEGER,

  atbats               INTEGER,
  runs                 INTEGER,
  hits                 INTEGER,
  doubles              INTEGER,
  triples              INTEGER,
  homeruns             INTEGER,
  rbi                  INTEGER,
  stolen_bases         INTEGER,
  caught_stealing      INTEGER,
  bb                   INTEGER,
  so                   INTEGER,
  ibb                  INTEGER,
  hbp                  INTEGER,
  sacfly               INTEGER,

  runs_per_ab          NUMERIC(16, 12),
  batting_avg          NUMERIC(16, 12),
  double_avg           NUMERIC(16, 12),
  triple_avg           NUMERIC(16, 12),
  hr_avg               NUMERIC(16, 12),
  rbi_avg              NUMERIC(16, 12),
  bb_avg               NUMERIC(16, 12),
  so_avg               NUMERIC(16, 12),
  ibb_avg              NUMERIC(16, 12),
  hbp_avg              NUMERIC(16, 12),
  sb_pct               NUMERIC(16, 12)

  embeddings_str       VARCHAR(255)
);

\d players
