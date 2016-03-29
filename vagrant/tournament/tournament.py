#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    command = "DELETE FROM Matches;"
    cursor.execute(command)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    command = "DELETE FROM Players;"
    cursor.execute(command)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    command = "SELECT COUNT(id) as numPlayers FROM Players;"
    cursor.execute(command)
    rows = cursor.fetchall()
    db.close()
    return rows[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    command = "INSERT INTO Players (name) VALUES (%s);"
    cursor.execute(command, (name,))
    db.commit()
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
    db = connect()
    cursor = db.cursor()
    command = "SELECT * FROM Standings ORDER BY Standings.wins DESC;"
    cursor.execute(command)
    rows = cursor.fetchall()
    db.close()
    return rows


def reportMatch(winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    command = "INSERT INTO Matches (player, opponent, result) VALUES (%s,%s,%s);"
    if draw:
        cursor.execute(command,(winner, loser, 1))
        cursor.execute(command,(loser, winner, 1))
    else:
        cursor.execute(command, (winner,loser,1))
        cursor.execute(command,(loser,winner,0))
    db.commit()
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
    standings = playerStandings()
    pairs = []
    for i in xrange(0, len(standings),2):
        player1id = standings[i][0]
        player1name = standings[i][1]
        player2id = standings[i+1][0]
        player2name = standings[i+1][1]
        pairs.append((player1id,player1name,player2id,player2name))
        i +=2
    print(pairs)
    return pairs

