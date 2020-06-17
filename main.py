from Suggestions import Suggestions
import sys
import pandas as pd
import spacy
import os
from flask import Flask, request, Response, render_template
import joblib
from sqlalchemy import create_engine
import configparser


user = os.getenv('POSTGRES_USER')
pwd = os.getenv('POSTGRES_PASS')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')



print("Attempt to connect to PSQL at {}:{} as user '{}'".format(host, port, user))
app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://'+user+':'+pwd+'@'+host+':'+port+'/whattowatch')

print("loading dfs")
df = pd.read_sql_query('select * from "TAGS"', con=engine)
df_titles_and_ratings = pd.read_sql_query('select * from "TITLES_AND_RATINGS"', con=engine)
print("loaded dfs")

print("loading model")
nlp = spacy.load('en_core_web_lg')
print("loaded model")

print("loading pickled file")
try:
    rv = joblib.load('update-database/filename.pickle')
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
print("loaded file")




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/suggest")
def Suggest():
    q = request.args.get('q')
    suggestions = Suggestions(df, df_titles_and_ratings, q, rv, nlp)
    result = suggestions.calculate_weigths()
    return result #TO OBTAIN JSON: Response(result.to_json(orient="records"), mimetype='application/json')



if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000, debug=True, threaded = True, use_reloader=False)
