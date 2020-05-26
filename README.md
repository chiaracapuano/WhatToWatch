# WhatToWatch
This repo contains the development of a simple Flask app, that suggests Netflix movie titles based on user input.\
The folder **update-database** contains the **main_updateDB.py** program, that should be run for update/creation of DB purposes.\ 
The DB is located in Postgres and is accessed via sqlalchemy. The connection details are contained in a login.config file, an example of which is available in login.config.example.\ 
The DB contains four tables:\
* TAGS: 
* TITLES:
* RATINGS:
* TITLES_AND_RATINGS: 
