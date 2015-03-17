#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import sys

DB_NAME = "tournament"


def connect(dbname=DB_NAME):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname="+dbname)

def db_transact(query,dbname=DB_NAME):
    """ Performs Db transaction: Connects to db, executes query, commits,closes connection.
        Returns db object. """

    db=None
                            
    try:
        db = connect(dbname)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        return db

    except psycopg2.DatabaseError, e:

        if db:
            db.rollback()
            
        print 'DB error...rolled back %s' % e
        sys.exit(1)

    finally:
        if db:
            db.close()
            
                            
    


def deleteMatches():
    """Remove all the match records from the database."""
    del_match_q = ' DELETE FROM matches '
    db_transact(del_match_q,DB_NAME)


def deletePlayers():
    """Remove all the player records from the database."""
    del_plyr_q = ' DELETE FROM players '
    db_transact(del_plyr_q,DB_NAME)


def countPlayers():
    """Returns the number of players currently registered."""
    count_q = ' SELECT COUNT(player_id) FROM players '

    db=None
                            
    try:
        db = connect(DB_NAME)
        cur = db.cursor()
        cur.execute(count_q)
        rows = cur.fetchall()
        return int(rows[0][0])

    except psycopg2.DatabaseError, e:

        if db:
            db.rollback()
            
        print 'DB error...rolled back %s' % e
        sys.exit(1)

    finally:
        if db:
            db.close()
            

    
    


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  
  
    Args:
      name: the player's full name (need not be unique).
    """

    name = bleach.clean(name)
    add_plyr_q = 'INSERT INTO players (player_name) VALUES (%s)'

    db=None
                            
    try:
        db = connect(DB_NAME)
        cur = db.cursor()
        cur.execute(add_plyr_q,(name,))
        db.commit()

    except psycopg2.DatabaseError, e:

        if db:
            db.rollback()
            
        print 'DB error...rolled back %s' % e
        sys.exit(1)

    finally:
        if db:
            db.close()
    


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    """ use the Views created to fetch the wins, loss. Then JOIN to get total.
        Query uses postgres feature Common table expressions (CTE) for ease of use
        Query uses COALESCE to substitute a default value for null values


    """


    plyr_stnd_q = ''' WITH player_standing AS (
                        SELECT COALESCE(win_player_id, lose_player_id) player_id, COALESCE(wins,0) wins, COALESCE(loss,0) loss, COALESCE(wins,0)+COALESCE(loss,0) total 
                        from winners FULL OUTER JOIN losers on win_player_id = lose_player_id )SELECT  players.player_id,player_name, COALESCE(wins,0) matches_won ,
                        COALESCE(total,0) total_matches
                        FROM players FULL OUTER JOIN player_standing ON players.player_id = player_standing.player_id; '''

    db=None
    player_stand_list=[]
                            
    try:
        db = connect(DB_NAME)
        cur = db.cursor()
        cur.execute(plyr_stnd_q)
        rows = cur.fetchall()

        for row in rows:
            player_stand_list.append(row)
        

        return player_stand_list

    except psycopg2.DatabaseError, e:

        if db:
            db.rollback()
            
        print 'DB error...rolled back %s' % e
        sys.exit(1)

    finally:
        if db:
            db.close()
            


    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    

    
    match_result_q = 'INSERT INTO matches (win_player_id,lose_player_id) VALUES (%s,%s)'

    db=None
                            
    try:
        db = connect(DB_NAME)
        cur = db.cursor()
        cur.execute(match_result_q,(winner,loser))
        db.commit()

    except psycopg2.DatabaseError, e:

        if db:
            db.rollback()
            
        print 'DB error...rolled back %s' % e
        sys.exit(1)

    finally:
        if db:
            db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    """ Steps: get ordered list of players and standings from player_standing method. Then transform """

    standings = playerStandings()
    pair_result = []

    if len(standings) % 2 != 0:
        raise KeyError("Need even number of players for pairing.")

    for i in xrange(0,len(standings),2):
        player1_id = standings[i][0]
        player1_name = standings[i][1]
        player2_id = standings[i+1][0]
        player2_name = standings[i+1][1]
        pair_result.append((player1_id,player1_name,player2_id,player2_name))


    return pair_result
        


