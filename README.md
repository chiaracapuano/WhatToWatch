# WhatToWatch
This repo contains the development of a simple Flask app, that suggests Netflix movie titles based on user input.

The app pulls data from a Postgres DB and suggests movie titles usign a pre-trained Natural Language Processing package offered by Python: SpaCy. The app is deployed in Docker.

***PART I*** 
* DB creation/update
* Flask App developement

The folder **update-database** contains the **main_updateDB.py** program, that should be run for update/creation of DB purposes.

The DB is located in Postgres and is accessed via sqlalchemy. The connection details are contained in a login.config file, an example of which is available in login.config.example.

The DB contains four tables:
* TAGS: produced by Scraper.py. The content of the Netflix movies website is scraped and at the same time Rake NLTK is used to extract the relevant words from the Netflix movie description (ignoring stop words and punctuation) and also from the Netflix movie tags. A line in the table consists in the movie web address on Netflix and a single keyword to describe it.
Also, this dataframe is pickled in Scraper.py: this move is necessary in that it will speed up the process of comparison between the user input word and the identified keywords when it will come to movie suggestions. 
* TITLES: produced by Movies_Titles.py. This table contains the Netflix web address of a specific movie and the movie title, both obtained by scraping the Netflix movie website. 
* RATINGS: produced by Rotten_Tomatoes.py. This table is obtained scraping the Rotten Tomatoes website to obtain the Tomatometer rating of the movies scraped from Netflix. The movie titles are obtained from the table TITLES and modified to suit the Rotten Tomatoes movie web addresses. 
* TITLES_AND_RATINGS: produced by Rotten_Tomatoes.py. This table contains the movies titles in displayed both in a user friendly manner (as per table TITLES) and Rotten Tomatoes website suitable, together with the Tomatometer rating.


**main.py** in the main folder contains the development of the Flask app. The movies suggestions are evaluated in Suggestions.py, where the user input words are compared, one by one, with the indivdual tags contained in the table TAGS. The semantic similarity is calculated by SpaCy (0-1 scale), and a similarity index is provided for each one of the tags with respect to the user search term: by taking the cube of the similarity indexes, as well as multiplying the indexes < 0.5 by 0.1, the low similarity indexes are punished.

Also, it is assumed that the first two search terms entered by the user are the most relevant for the comparison with the tags, therefore the similarity indexes calculatedfor the first search term are multiplied by 2, for the second term by 1.5. 

The indexes obtained are averaged across the movie titles, and in output the top 5 suggestions are provided in json format, containing the movies title, Netflix link and Tomatometer rating.

The json format is required to accommodate for furture plans of transformin the Flask app in an Angular based webapp.

***PART II*** 
* Creation of Docker containers

Two containers are built and run: a container for the Postgres DB and a container for the Flas app. They are subsequently linked together.

The Postgres container is built via the Dockerfile contained in the folder **psql**, executing the commands:

_docker build -f ./psql/Dockerfile -t <DOCKERHUB_POSTGRES_CONTAINER> ./psql/_

and 

*docker run --rm -d  --name <NAME> -v ${HOME}/postgres-data/:/var/lib/postgresql/data  -p <POSTGRES_LOCAL_PORT>:<DOCKERHUB_POSTGRES_CONTAINER_PORT>  <DOCKERHUB_POSTGRES_CONTAINER>*

Run **main_updateDB.py** connecting to the container's address to populate the Postgres DB.

The flask container is built via:

*docker build -t <DOCKERHUB_FLASK_CONTAINER>  .*

The containers are linked together:

*docker run -it -p 5000:5000 --link <NAME> -e POSTGRES_PORT=<DOCKERHUB_POSTGRES_CONTAINER_PORT> -e POSTGRES_HOST=<NAME> -e POSTGRES_PASSWORD=<PWD> <DOCKERHUB_FLASK_CONTAINER>*


