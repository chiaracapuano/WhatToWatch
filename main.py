from Suggestions import Suggestions
import sys
import pandas as pd
import spacy
from flask import Flask, request
import joblib
import streamlit as st

df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")
df_title = pd.read_csv(r'./Movie_Titles_Ratings.csv', encoding="utf-8")

app = Flask(__name__)



#nlp = get_model()

@app.route("/")
def home():
    return """
    <html><head></head>
    <body>
        <h1>Fuck you and the horse</h1>
        <h3>you rode in on</h3>
        <div>
            <form action="/api/suggest" method="get">
                <label for="q">Query:</label><br>
                <input type="text" id="q" name="q" value=""><br>
            </form>
        </div>
        </body>
    </html>
           """

@app.route("/api/suggest")
def Suggest():
    q = request.args.get('q')
   # load_model()
    #rv = get_file()


    suggestions = Suggestions(df, df_title, q, rv, nlp)
    return suggestions.display_results()
    #    output=model.predict(data)  #what you want to do with frozen model goes here"""


if __name__ == "__main__":
    @st.cache()
    def load_model(name):
        return spacy.load(name)


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
    print(("* Loading NLP model and Flask starting server..."
           "please wait until server has fully started"))


    app.run(debug=True, threaded = True)



