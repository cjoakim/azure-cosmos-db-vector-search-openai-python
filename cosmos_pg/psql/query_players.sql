-- query_players.sql
-- query a few of the primary example players in the database
-- Chris Joakim, Microsoft 

select * from players where player_id in ('aaronha01', 'rosepe01', 'jeterde01', 'henderi01', 'blombro01', 'guidrro01')
