Project 2: Swiss Tournament 
=============

A database-backed Python module to run a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.
The goal of the Swiss pairings system is to pair each player with an opponent who has won the same number of matches, or as close as possible.

###Assumptions in the current version:
- Supports only one tournament at present
- the number of players in a tournament is an even number. This means that no player will be left out of a round.

###Contains 3 modules:
1.Simple postgres DB to store the game matches between players based on swiss tournament rules. 
2.The tournament.py that contains functions that is use to query the db , insert and update results.
3.Tournament_tests.py has tests for various scenarios.

### Running the modules:
- The vagrant file setups the required packages/libraries. The pg_config has the table and view creation DDLs that will be run when vagrant provision process happens
- Note: Tests  are setup to wipe out data as part of testing various scenariosS
