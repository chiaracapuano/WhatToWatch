# WhatToWatch
This repo contains the development of a simple Flask app, that suggests Netflix movie titles based on user input.

The app pulls movie tags and titles from a Postgres DB, evaluates the semantic similarity between user input words and tags using Python SpaCy and displays the suggestions in a table that shows the top 5 movies identified and their Tomatometer rating. 

The app is containerized in Docker and deployed to Kubernetes.

Here an **example of homepage**:

![alt text](https://github.com/chiaracapuano/WhatToWatch/blob/master/png-example/home-page.png)

and **output** as produced by the app, when the topic is *scientists*:

![alt text](https://github.com/chiaracapuano/WhatToWatch/blob/master/png-example/output.png)

The following sections of the README discuss respectively the Python codebase, Docker and Kubernetes files and commands:

[1. Python-Code](#1. Python-Code)

[2. Docker-Files](#Docker)

[3. Kubernetes-Files](#Kubernetes)

### 1. Python-Code
Folders:
* home folder
* update-database
* templates

#### home folder

**main.py** in the home folder contains the development of the Flask app. 

The movies suggestions are evaluated in **Suggestions.py**, where the user input words are compared, one by one, with the indivdual tags contained in the table TAGS. The semantic similarity is calculated by SpaCy (0-1 scale), and a similarity index is provided for each one of the tags with respect to the user search term: by taking the cube of the similarity indexes, as well as multiplying the indexes < 0.5 by 0.1, the low similarity indexes are punished.

Also, it is assumed that the first two search terms entered by the user are the most relevant for the comparison with the tags, therefore the similarity indexes calculatedfor the first search term are multiplied by 2, for the second term by 1.5. 

The indexes obtained are averaged across the movie titles, and in output the top 5 suggestions are provided in json format, containing the movies title, Netflix link and Tomatometer rating.

The library Jinja 2 is used to render the dataframe in output.

#### update-database

The folder **update-database** contains the **main_updateDB.py** program, that should be run for update/creation of DB purposes.

The DB is located in Postgres and is accessed via sqlalchemy. The connection details are contained in a login.config file, an example of which is available in login.config.example, and are accessed using env variables.

The DB contains four tables:
* TAGS: produced by **Scraper.py**. The content of the Netflix movies website is scraped and at the same time Rake NLTK is used to extract the relevant words from the Netflix movie description (ignoring stop words and punctuation) and also from the Netflix movie tags. A line in the table consists in the movie web address on Netflix and a single keyword to describe it.
Also, this dataframe is pickled in Scraper.py: this move is necessary in that it will speed up the process of comparison between the user input word and the identified keywords when it will come to movie suggestions. 
* TITLES: produced by **Movies_Titles.py**. This table contains the Netflix web address of a specific movie and the movie title, both obtained by scraping the Netflix movie website. 
* RATINGS: produced by **Rotten_Tomatoes.py**. This table is obtained scraping the Rotten Tomatoes website to obtain the Tomatometer rating of the movies scraped from Netflix. The movie titles are obtained from the table TITLES and modified to suit the Rotten Tomatoes movie web addresses. 
* TITLES_AND_RATINGS: produced by Rotten_Tomatoes.py. This table contains the movies titles in displayed both in a user friendly manner (as per table TITLES) and Rotten Tomatoes website suitable, together with the Tomatometer rating.

#### templates

The folder **templates** contains:
* **home.html**: file that renders the home page of the Flask app
* **output.html**: file that renders the dataframe visualized in output as movie suggestions.



### Docker

Two containers are built and run: 
* Flask app container 
* Postgres DB container -> *not needed for the Kubernetes deployment*, but for the containers linkage: the containers are linked together simply becuase I was curious to know if I could make it work.

#### Postgres DB container 

The Postgres container is built via the Dockerfile contained in the folder **psql**, executing the commands:

```
docker build -f ./psql/Dockerfile -t <DOCKERHUB_POSTGRES_CONTAINER> ./psql/
```

and 

```
docker run --rm -d  --name <NAME> -v ${HOME}/postgres-data/:/var/lib/postgresql/data  -p <POSTGRES_LOCAL_PORT>:<DOCKERHUB_POSTGRES_CONTAINER_PORT>  <DOCKERHUB_POSTGRES_CONTAINER>
```
  
The respective Dockerfile can be found on the Docker official documentation at: 

https://docs.docker.com/engine/examples/postgresql_service/

Run **main_updateDB.py** connecting to the container's address to populate the Postgres DB, or simply dump the local DB to the Docker DB using a dump (I use DataGrip to do this).

#### Flask app container 

The flask container is built via:

```
docker build -f ./docker_files/Dockerfile -t <DOCKERHUB_FLASK_CONTAINER>  ./docker_files/
```

The containers are linked together:

```
docker run -it -p 5000:5000 --link <NAME> -e POSTGRES_PORT=<DOCKERHUB_POSTGRES_CONTAINER_PORT> -e POSTGRES_HOST=<NAME> -e POSTGRES_PASSWORD=<PWD> <DOCKERHUB_FLASK_CONTAINER>
```
  
The respective Dockerfile contains a list of libraries to be installed for the Flask app to work in the container. Some of the libraries are included in the file **requirements.txt**.

### Kubernetes

Two pods are built and run: 
* Postgres DB pod 
* Flask app pod

#### Postgres DB pod  

The files necessary to create this pod are contained in the **infrastructure** subfolder. The files are produced based on the tutorial: 

https://severalnines.com/database-blog/using-kubernetes-deploy-postgresql

The command run to deploy the DB is: 

```
kf apply -f ./kubernetes_files/infrastructure/
```

The DB is populated simply copying the local Postgres DB of interest in the Kubernetes Postgres instance (I use DataGrip to do this).

#### Flask app pod

The files necessary to spin up the pod are based on the tutorial:

https://www.conjur.org/blog/tutorial-spin-up-your-kubernetes-in-docker-cluster-and-they-will-come/

and they rely on the Dockerhub image of the Flask app produced in the previous step (#Docker).

The pod is deployed via:

```
kf apply -f ./kubernetes_files/app/ 
```

and the app is run via:

```
kc logs -f --tail=-1 -l app=whattowatch --all-containers=true  
```




