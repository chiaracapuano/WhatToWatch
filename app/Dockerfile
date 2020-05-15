FROM tiangolo/uwsgi-nginx-flask:python3.6
RUN pip install -r requirements.txt
CMD python main.py

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