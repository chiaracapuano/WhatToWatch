from app.Suggestions import Suggestions
import sys
import pandas as pd
import spacy
from flask import Flask, request
import joblib
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:dasquee@localhost:5432/WhatToWatch')


def dfs_update(update_dbs = False, write_to_csv = False):
    if update_dbs == True:
        from app.Scraper import Scraped_Tags
        from app.Movies_Titles import Movie_Titles
        from app.Rotten_Tomatoes import Ratings

        updated_df = Scraped_Tags()
        df = updated_df.scrape_and_tag()
        df.to_sql('TAGS', engine, if_exists = 'replace')
        print("TAGS have been updated and picled")

        df = pd.read_sql_query('select * from "TAGS"', con=engine)
        updated_titles = Movie_Titles(df)
        df_titles = updated_titles.get_titles()
        df_titles.to_sql('TITLES', engine, if_exists = 'replace')
        print("TITLES have been updated")

        ratings = Ratings(df_titles)
        df_ratings = ratings.get_ratings()
        df_ratings.to_sql('RATINGS', engine, if_exists = 'replace')
        print("RATINGS have been updated")

        if write_to_csv==True:
            tags_df_loc = r'./Netflix_Movies_All_Tags.csv'
            df.to_csv(tags_df_loc, index=False)
            title_df_loc = r'./Movie_Titles.csv'
            df_titles.to_csv(title_df_loc, index=False)
            ratings_df_loc = r'./Movie_Titles_Ratings.csv'
            df_ratings.to_csv(ratings_df_loc, index = False)
    else:
        print("DBs have not been updated")

dfs_update()
df = pd.read_sql_query('select * from "TAGS"',con=engine)
df_ratings = pd.read_sql_query('select * from "RATINGS"',con=engine)
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


    print(("* Loading NLP model and Flask starting server..."
           "please wait until server has fully started"))


    app.run(debug=True, host='0.0.0.0', threaded = True)