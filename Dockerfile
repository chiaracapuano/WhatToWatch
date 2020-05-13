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