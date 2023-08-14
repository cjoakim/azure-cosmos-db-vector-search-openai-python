-- query_batters.sql
-- Chris Joakim, Microsoft 

select id, player_id, first_name, last_name, homeruns, stolen_bases, sb_pct, debut_year from batters
where homeruns > 100
and   stolen_bases > 500
and   sb_pct > 0.80
order by stolen_bases desc;
