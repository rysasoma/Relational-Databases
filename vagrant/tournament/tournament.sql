-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


-- Tournaments Table
CREATE TABLE IF NOT EXISTS Tournaments (
	id SERIAL primary key,
	name VARCHAR(255)
);

-- Players Table
CREATE TABLE IF NOT EXISTS Players (
	id SERIAL primary key,
	name varchar(255)
);

-- Matches Table
CREATE TABLE IF NOT EXISTS Matches (
	id SERIAL primary key,
	tournament INTEGER references Tournaments(id),
	winner INTEGER references Players(id),
	loser INTEGER references Players(id),
	draw BOOLEAN 
);


-- TournamentPlayerRegistry Table
CREATE TABLE IF NOT EXISTS TournamentPlayerRegistry (
	tournament INTEGER references Tournaments(id),
	player INTEGER references Players(id),
	bye INTEGER,
	PRIMARY KEY(tournament, player)	
);

-- ScoreCard Table
CREATE TABLE IF NOT EXISTS ScoreCard (
	tournament INTEGER references Tournaments(id),
	player INTEGER references Players(id),
	score INTEGER,
	matches INTEGER,
	bye INTEGER,
	PRIMARY KEY(tournament, player)
);

-- add tournament attribute to players, wintracker and matchtracker.  Then add tournament to standings where %s is specified and in select part.
-- Wintracker View joins matches and tournamentplayerregistry tables to count the number of wins by player
CREATE VIEW wintracker AS
SELECT TournamentPlayerRegistry.tournament, Players.id, Players.name, COUNT(Matches.winner) AS wins
FROM Players LEFT JOIN TournamentPlayerRegistry ON Players.id = TournamentPlayerRegistry.player 
LEFT JOIN Matches ON TournamentPlayerRegistry.player = matches.winner AND TournamentPlayerRegistry.tournament = Matches.tournament
GROUP BY TournamentPlayerRegistry.tournament, TournamentPlayerRegistry.player;




-- Matchtracker View joins matches and tournamentplayerregistry tables to count the number of matches by player
CREATE VIEW matchtracker AS
SELECT TournamentPlayerRegistry.tournament, Players.id, Players.name, COUNT(matches) AS matchesPlayed
FROM Players LEFT JOIN TournamentPlayerRegistry ON Players.id = TournamentPlayerRegistry.player 
LEFT JOIN Matches ON (TournamentPlayerRegistry.player = matches.winner OR TournamentPlayerRegistry.player = matches.loser) 
AND TournamentPlayerRegistry.tournament = Matches.tournament
GROUP BY TournamentPlayerRegistry.tournament, TournamentPlayerRegistry.player;




-- Standings View which joins wintracker and matchtracker to display
-- player's id, name, wins, matches played
-- view is used to display players standings as well as create new matchups based on totals 
CREATE VIEW standings AS 
SELECT wintracker.id, wintracker.name, wintracker.wins, matchtracker.matchesPlayed, 
(SELECT SUM(w2.wins) 
    FROM wintracker as w2 WHERE 
        w2.id IN (SELECT loser FROM Matches WHERE winner = w1.id AND matches.tournament = w2.tournament AND matches.tournament = w1.tournament)
        OR w2.id IN (SELECT winner FROM Matches WHERE loser = w1.id and matches.tournament = w2.tournament AND matches.tournament = w1.tournament)) as omw
FROM wintracker JOIN matchtracker as w1 ON wintracker.id = matchtracker.id 
AND wintracker.tournament = matchtracker.tournament ORDER BY w1.wins DESC, omw DESC, w1.matchesPlayed;
