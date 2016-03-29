#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteScoreCard():
    """Remove all the score records from the database """
    db = connect()
    cursor = db.cursor()
    command = "DELETE FROM ScoreCard;"
    cursor.execute(command)
    db.commit()
    db.close()


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


def deleteTournaments():
    """Remove all the tournament records from the database. """
    db = connect()
    cursor = db.cursor()
    command = "DELETE FROM Tournaments;"
    cursor.execute(command)
    db.commit()
    db.close()


def createTournament(name):
    """ 
    Create a new tournament
    @name: Name of the tournament
    Returns the tournament id.
    """
    db = connect()
    cursor = db.cursor()
    command = "INSERT INTO tournaments (name) VALUES (%s) RETURNING id;"
    cursor.execute(command, (name,))
    tournamentId = cursor.fetchone()[0]
    db.commit()
    db.close()
    return tournamentId


def countPlayers(tournamentId):
    """
    Returns the number of players currently registered in the given tournament.
    @tournamentId: The id of the tournament we are looking for players in.
    """
    db = connect()
    cursor = db.cursor()
    command = "SELECT COUNT(player) FROM ScoreCard WHERE tournament = %s;"
    cursor.execute(command, (tournamentId,))
    count = cursor.fetchone()[0]
    db.close()
    return count


def registerPlayer(name, tournamentId):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    command = "INSERT INTO Players (name) VALUES (%s) RETURNING id;"
    cursor.execute(command, (name,))
    playerId = cursor.fetchone()[0]
    command = "INSERT INTO ScoreCard (tournament, player, score, matches, bye) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(command, (tournamentId, playerId, 0, 0, 0))
    db.commit()
    db.close()


def playerStandings(tournamentId):
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
    command = """SELECT s.player, Players.name, s.score, s.matches, s.bye, (SELECT SUM(s2.score) 
	       FROM ScoreCard as s2 
               WHERE s2.player IN 
               (SELECT loser FROM Matches WHERE winner = s.player AND tournament = %s) 
 	       OR s2.player IN 
	       (SELECT winner FROM Matches WHERE loser = s.player AND tournament = %s)) AS omw 
	       FROM ScoreCard as s JOIN Players ON s.player = Players.id 
	       WHERE s.tournament = %s ORDER BY s.score DESC, omw DESC, s.matches;"""
    cursor.execute(command, (tournamentId, tournamentId, tournamentId))
    standings = []
    for standing in cursor.fetchall():
        standings.append(standing)
    db.close()
    return standings


def reportMatch(tournamentId, winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if draw == 'TRUE':
        winnerPts = 1
        loserPts = 1
    else:
        winnerPts = 2
        loserPts = 0

    db = connect()
    cursor = db.cursor()
    command = "INSERT INTO Matches (tournament, winner, loser, draw) VALUES (%s,%s,%s,%s);"
    cursor.execute(command, (tournamentId, winner, loser, draw))
    command = "UPDATE ScoreCard SET score = score+%s, matches = matches+1 WHERE player = %s AND tournament = %s;"
    cursor.execute(command, (winnerPts, winner, tournamentId))
    command = "UPDATE ScoreCard SET score = score+%s, matches = matches+1 WHERE player = %s AND tournament = %s;"
    cursor.execute(command, (loserPts, loser, tournamentId))
    db.commit()
    db.close()


def canBye(tournamentId, playerId):
    """
    Checks if the player has a bye.
    @tournamentId: ID of the tournament
    @playerId: ID of the player
    """
    db = connect()
    cursor = db.cursor()
    command = "SELECT bye FROM ScoreCard WHERE tournament = %s AND player = %s;"
    cursor.execute(command, (tournamentId, playerId))
    canBye = cursor.fetchone()[0]
    db.close()
    if canBye:
        return True
    return False


def reportBye(tournamentId, playerId):
    """
    Reports a bye for a player in a specific tournament
    @tournamentId: The id of the tournament.
    @playerId: The id of the player.
    """
    db = connect()
    cursor = db.cursor()
    command = "UPDATE ScoreCard SET score = score + 2, matches = matches + 1, bye = bye + 1 WHERE tournament = %s AND player = %s;"
    cursor.execute(command, (tournamentId, playerId))
    db.commit()
    db.close()


def checkByes(tournamentId, standings, playerStanding):
    """
    Checks if the player already has a bye
    @tournamentId: the id of the current tournament
    @standings: the standings of the players in the current tournament
    @playerStanding: the index of the player in the standings
    Returns the first index of player without bye or -1 if every player has had a bye.
    """
    if playerStanding > len(standings):
        return -1
    elif not canBye(tournamentId, standings[playerStanding][0]):
        return playerStanding
    else:
        return checkByes(tournamentId, standings, playerStanding + 1)


def validPair(tournamentId, player1, player2):
    """
    Checks if two players have played each other already
    @tournamentId: The id of the current tournament
    @player1: The id of the first player
    @player2: The id of the second player
    Returns whether the pairing is valid.
    """
    db = connect()
    cursor = db.cursor()
    command = "SELECT winner, loser FROM Matches WHERE ((winner = %s AND loser = %s) OR (winner = %s AND loser = %s)) AND tournament = %s;"
    cursor.execute(command, (player1, player2, player2, player1, tournamentId))
    prevMatches = cursor.rowcount
    db.close()
    if prevMatches > 0:
        return False
    return True


def checkPairs(tournamentId, standings, player1, player2):
    """
    Checks if two players have had a match already and recursively finds new pairings if they have already played
    each other. 
    @tournamentId: the id of the current tournament
    @standings: the current rankings of the players
    @player1: the index of the first player to be paired
    @player2: the index of the second player to be paired
    Returns the id of the matched player or the original match if a new pairing is not found. 
    """
    if player2 >= len(standings):
        return player1+1
    elif validPair(tournamentId, standings[player1][0], standings[player2][0]):
        return player2
    else:
        return checkPairs(tournamentId, standings, player1, (player2+1))


def swissPairings(tournamentId):
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
    standings = playerStandings(tournamentId)
    pairs = []
    playerCount = countPlayers(tournamentId)
    if playerCount % 2 != 0:
        bye = standings.pop(checkByes(tournamentId, standings, 0))
        reportBye(tournamentId, bye[0])

    while len(standings) > 1:
        validMatch = checkPairs(tournamentId, standings, 0, 1)
        player1 = standings.pop(0)
        player2 = standings.pop(validMatch - 1)
        pairs.append((player1[0], player1[1], player2[0], player2[1]))

    return pairs
