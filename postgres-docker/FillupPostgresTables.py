import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://Python-App:1234@postgres:5433/WhatToWatch') #f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'


from Scraper import Scraped_Tags
from Movies_Titles import Movie_Titles
from Rotten_Tomatoes import Ratings

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



