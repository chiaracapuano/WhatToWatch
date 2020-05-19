FROM achiaracapuano/nlp-python-base:nlp-3.7.6-buster
#FROM python:3.7.6-buster
COPY app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install spacy
RUN python -m spacy download en_core_web_lg
RUN pip install -r requirements.txt
RUN pip install pandas
RUN pip install requests

EXPOSE 5000
CMD python ./main.py


#docker build -t python-app/dev .
#docker run -e DB_PORT=5432 -e DB_HOST=docker.for.mac.host.internal
#psql postgresql://postgres:dasquee@localhost:5432/WhatToWatch


