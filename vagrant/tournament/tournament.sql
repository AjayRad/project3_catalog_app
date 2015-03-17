-- Table definitions for the tournament project.
-- Create DDL statements to create 2 of the primary tables : players, matches 

CREATE TABLE players   ( player_id serial primary key,
                         player_name varchar (40) not null,
                         last_updated_ts timestamp default current_timestamp);
                            
CREATE TABLE matches    ( match_id serial primary key,
                         win_player_id int,
                         lose_player_id int,
                        foreign key(win_player_id) references players(player_id),
                         foreign key(lose_player_id) references players(player_id),
                         tourn_id int,
                         foreign key(tourn_id) references tournament(tourn_id),
                         last_updated_ts timestamp default current_timestamp);
 
-- Create DDL for the tournament table 
 
CREATE TABLE tournament ( tourn_id serial primary key,
                         tournament_name varchar(50) not null,
                         last_updated_ts timestamp default current_timestamp);
                          


-- Views to help group winners and loser within the MATCHES table
-- NOTE: the views are similar except that the aggregation are on two different columns on the same table 

CREATE OR REPLACE VIEW winners AS SELECT WIN_PLAYER_ID, COUNT(*) AS WINS FROM matches GROUP BY WIN_PLAYER_ID ORDER BY WINS DESC;
CREATE OR REPLACE VIEW losers AS SELECT LOSE_PLAYER_ID, COUNT(*) AS LOSS FROM matches GROUP BY LOSE_PLAYER_ID ORDER BY LOSS DESC;

