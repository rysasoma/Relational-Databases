-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


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


-- Scores Table
CREATE TABLE IF NOT EXISTS ScoreCard (
	tournament INTEGER references Tournaments(id),
	player INTEGER references Players(id),
	score INTEGER,
	matches INTEGER,
	bye INTEGER,
	PRIMARY KEY(tournament, player)	
);
