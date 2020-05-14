FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY requirements.txt /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

COPY app/ /app/

WORKDIR /app

ENV FLASK_APP=main.py
CMD flask run -h 0.0.0.0 -p 5000
#COPY . /app
#WORKDIR /app
#RUN pip install --upgrade pip
#RUN pip install spacy
#RUN python -m spacy download en_core_web_lg
#RUN pip install -r requirements.txt
#RUN pip install pandas
#RUN pip install requests

#EXPOSE 5000
#CMD python ./main.py


#docker build -t docker-flask-sample .
#docker run -it --env DBPASS="<PASSWORD>" --env DBHOST="<SERVER_HOST_NAME>" --env DBUSER="<USERNAME>" --env DBNAME="<DATABASE_NAME>" -p 5000:5000 docker-flask-sample
#docker run -it --env DBPASS="dasquee"  --env DBUSER="postgres" --env DBNAME="WhatToWatch" -p 5000:5000 docker-flask-sample