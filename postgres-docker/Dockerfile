FROM postgres:latest

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.7-dev
RUN apt-get install libpq-dev g++ python3-dev musl-dev
RUN pip3 install psycopg2
RUN pip3 install pandas
RUN pip3 install --upgrade pip
RUN pip3 install spacy
RUN python3 -m spacy download en_core_web_lg
RUN pip3 install bs4
RUN pip3 install requests
RUN pip3 install wheel
RUN pip3 install psycopg2-binary
RUN pip3 install SQLAlchemy
RUN pip3 install pandas
RUN pip3 install requests
RUN pip3 install rake_nltk
RUN pip3 install unidecode
RUN pip3 install flask
RUN pip3 install joblib
RUN pip3 install wheel
RUN pip3 install SQLAlchemy
RUN python3 -m nltk.downloader punkt













# add the 'postgres' admin role
USER postgres

# expose Postgres port
EXPOSE 5432

# bind mount Postgres volumes for persistent data
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

#docker build -t python-app/dev .
#docker run -e DB_PORT=5432 -e DB_HOST=docker.for.mac.host.internal
#psql postgresql://postgres:dasquee@localhost:5432/WhatToWatch


