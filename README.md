# Udacity-FullStack-Project-2
A basic schema for a swiss tournament.

#Pre-requisites
1. Need PostgreSQL

2. Need SQLite 

3. Need python

#Usage
Have a tournament database 


    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
    psql (9.3.5)
    Type "help" for help.
    
    vagrant=> CREATE DATABASE tournament;
    CREATE DATABASE
    vagrant=> \q

Load the SQL schema
    
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql tournament < tournament.sql

Run python tests!

    python tournament_test.py

