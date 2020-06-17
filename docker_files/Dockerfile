FROM achiaracapuano/nlp-python-base:nlp-3.7.6-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install spacy
RUN python -m spacy download en_core_web_lg
RUN pip install -r ./requirements.txt
RUN pip install pandas
RUN pip install requests

EXPOSE 5000
CMD python ./main.py


