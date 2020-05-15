FROM python:3.7.6-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install spacy
RUN python -m spacy download en_core_web_lg
RUN pip install -r requirements.txt
RUN pip install pandas
RUN pip install requests

EXPOSE 5000
CMD python ./main.py


#docker build -t my-python-app/dev .
#docker run -it -p 5000:5000 my-python-app/dev
#ENV FLASK_APP=main.py
#CMD flask run -h 0.0.0.0 -p 5001
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
#docker run -it --env DBPASS="dasquee" --env DBHOST="localhost" --env DBUSER="postgres" --env DBNAME="WhatToWatch" -p 5001:5000 docker-flask-sample