-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW IF EXISTS OMW;
DROP VIEW IF EXISTS Standings;
DROP View IF EXISTS playermatches;
DROP VIEW IF EXISTS Wins;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Players;

-- Players Table
CREATE TABLE Players (
	id SERIAL primary key,
	name varchar(255)
);

-- Matches Table
CREATE TABLE Matches (
	id SERIAL primary key,
	player int references Players(id),
	opponent int references Players(id),
	result int
);

-- Wins View shows number of wins for each Player
CREATE VIEW Wins AS
	SELECT Players.id, COUNT(Matches.opponent) AS n 
	FROM Players
	LEFT JOIN (SELECT * FROM Matches WHERE result>0) as Matches
	ON Players.id = Matches.player
	GROUP BY Players.id;

-- Count View shows number of matches for each Player
CREATE VIEW playermatches AS
	SELECT Players.id, Count(Matches.opponent) AS n 
	FROM Players
	LEFT JOIN Matches
	ON Players.id = Matches.player
	GROUP BY Players.id;

-- Standings View shows number of wins and matches for each Player
CREATE VIEW Standings AS 
	SELECT Players.id,Players.name,Wins.n as wins, playermatches.n as matches 
	FROM Players, playermatches, Wins
	WHERE Players.id = Wins.id and Wins.id = playermatches.id;

-- OMW Standings shows number of "Opponent Match Wins" for each Player
CREATE VIEW OMW AS
	SELECT Players.id, SUM(Standings.wins) as opponentMatchWins
	FROM Players, Matches, Standings
	WHERE Players.id = Matches.player AND Matches.opponent = Standings.id
	GROUP BY Players.id
