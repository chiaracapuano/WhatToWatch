from Rotten_Tomatoes import Ratings
from Scraper import Scraped_Tags
from Movies_Titles import Movie_Titles
import pandas as pd

class Update_dfs:

    def __init__(self, engine):
        self.engine = engine
        self.refresh_on_start = False

    def obtain_dfs(self):
        con = self.engine.connect()

        try:
            self.refresh_on_start = con.execute('SELECT value from app where key=\'refreshDbOnStart\'')
        except:
            print("Exception reading from App table, this must be 'first run'")
            self.refresh_on_start = True
            con.execute('create table app ( key varchar not null, value varchar)')
            con.execute('INSERT INTO app (key, value) VALUES (\'refreshDbOnStart\', \'false\')')
            print("App Table created")

        if self.refresh_on_start:
            refresh_on_start = self.refresh_on_start
            print("Refreshing DB Tables")

            #scraped_tags = Scraped_Tags(refresh_on_start, con)
            #scraped_tags.scrape_and_tag()

            df = pd.read_sql_query('select * from "TAGS"', con=self.engine)
            movie_titles = Movie_Titles(df, refresh_on_start, con)
            movie_titles.get_titles()

            df_titles = pd.read_sql_query('select * from "TITLES"', con=self.engine)
            ratings = Ratings(df_titles, refresh_on_start, con)
            ratings.get_ratings()


