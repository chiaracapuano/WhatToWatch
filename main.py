from Suggestions import Suggestions
import sys
import pandas as pd
import spacy
from flask import Flask, request, Response
import joblib
from sqlalchemy import create_engine
import configparser

configParser = configparser.RawConfigParser()
configFilePath = './login.config'
configParser.read(configFilePath)
user = configParser.get('dev-postgres-config', 'user')
pwd = configParser.get('dev-postgres-config', 'pwd')
host = configParser.get('dev-postgres-config', 'host')
port = configParser.get('dev-postgres-config', 'port')

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://'+user+':'+pwd+'@'+host+':'+port+'/whattowatch')


df = pd.read_sql_query('select * from "TAGS"', con=engine)
df_ratings = pd.read_sql_query('select * from "TITLES_AND_RATINGS"', con=engine)

print("loaded dfs")
#docker push achiaracapuano/postgres:dev

print("loading model")
nlp = spacy.load('en_core_web_lg')
print("loaded model")
print("loading file")
try:
    rv = joblib.load('update-database/filename.pickle')
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
print("loaded file")




@app.route("/")
def home():
    return """
    <html><head></head>
    <style> 
            body { 
                text-align:center; 
            } 
            h1 { 
                color:green; 
            } 
        </style>
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
    result = suggestions.calculate_weigths()
    return Response(result.to_json(orient="records"), mimetype='application/json')



if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000, debug=True, threaded = True, use_reloader=False)
