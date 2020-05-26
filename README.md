# WhatToWatch
This repo contains the development of a simple Flask app, that suggests Netflix movie titles based on user input.

The folder **update-database** contains the **main_updateDB.py** program, that should be run for update/creation of DB purposes.

The DB is located in Postgres and is accessed via sqlalchemy. The connection details are contained in a login.config file, an example of which is available in login.config.example.

The DB contains four tables:
* TAGS: produced by Scraper.py. The content of the Netflix movies website is scraped and at the same time Rake NLTK is used to extract the relevant words from the Netflix movie description (ignoring stop words and punctuation) and also from the Netflix movie tags. A line in the table consists in the movie web address on Netflix and a single keyword to describe it.
Also, this dataframe is pickled in Scraper.py: this move is necessary in that it will speed up the process of comparison between the user input word and the identified keywords when it will come to movie suggestions. 
* TITLES: produced by Movies_Titles.py. This table contains the Netflix web address of a specific movie and the movie title, both obtained by scraping the Netflix movie website. 
* RATINGS: produced by Rotten_Tomatoes.py. This table is obtained scraping the Rotten Tomatoes website to obtain the Tomatometer rating of the movies scraped from Netflix. The movie titles are obtained from the table TITLES and modified to suit the Rotten Tomatoes movie web addresses. 
* TITLES_AND_RATINGS: produced by Rotten_Tomatoes.py. This table contains the movies titles in displayed both in a user friendly manner (as per table TITLES) and Rotten Tomatoes website suitable, together with the Tomatometer rating.
