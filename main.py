from Suggestions import Suggestions
import sys
import pandas as pd
import spacy
from flask import Flask, request
import joblib
from sqlalchemy import create_engine
import os


host = 'dev-postgres'
port = '5432'
print(host, port)
engine = create_engine('postgresql+psycopg2://dev_postgres:dasquee@localhost:5434/whattowatch')


df = pd.read_sql_query('select * from "TAGS"', con=engine)
df_ratings = pd.read_sql_query('select * from "TITLES_AND_RATINGS"', con=engine)

print("loaded dfs")

app = Flask(__name__)
print("loading model")
nlp = spacy.load('en_core_web_lg')
print("loaded model")
print("loading file")
try:
    rv = joblib.load('filename.pickle')
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
print("loaded file")
@app.route("/")
def home():
    return """
    <html><head></head>
    <body>
        <h1>Please enter a topic you'd like to watch a movie about</h1>
        <h3>Movies obtained from https://www.netflix.com/browse/genre/34399</h3>
        <div>
            <form action="/api/suggest" method="get">
                <label for="q">Topic:</label><br>
                <input type="text" id="q" name="q" value=""><br>
            </form>
        </div>
        </body>
    </html>
           """

@app.route("/api/suggest")
def Suggest():
    q = request.args.get('q')
    suggestions = Suggestions(df, df_ratings, q, rv, nlp)
    return suggestions.calculate_weigths()


if __name__ == "__main__":
    app.run(debug=True, threaded = True)