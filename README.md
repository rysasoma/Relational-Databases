# Udacity-FullStack-Project-2
A basic schema for a swiss style tournament.
[Description](https://en.wikipedia.org/wiki/Swiss-system_tournament) of a swiss tournament can be found here.

#Pre-requisites
1. Need PostgreSQL
2. Need SQLite 
3. Need python

OR

Use the Udacity environment by following the instructions [here](https://www.udacity.com/wiki/ud197/install-vagrant)

#How to Run
Have a tournament database 


    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
    psql (9.3.5)
    Type "help" for help.
    
    vagrant=> CREATE DATABASE tournament;
    CREATE DATABASE
    vagrant=> \q

Load the SQL schema for the first time with:
    
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql tournament < tournament.sql

Run the python tests with the following command:

    python tournament_test.py

