import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode
import urllib.request
class Ratings:
    def __init__(self, titles_df, refresh_on_start, engine):
        self.df = titles_df
        self.refresh_on_start = refresh_on_start
        self.engine = engine



    def get_ratings(self):
        """Obtain movies titles from the TITLES database.
        Modifies the titles to adapt to the Rotten Tomatoes website standard.
        Returns a DF that will be pushed to PSQL, containing titles and ratings."""
        if self.refresh_on_start == True:
            con = self.engine.connect()
            con.execute('drop table if exists RATINGS_OLD')

            con.execute('alter table if exists RATINGS rename to RATINGS_OLD')
            con.execute('create table RATINGS ( Code varchar not null, Title varchar, Title_to_merge varchar, Rating varchar)')

            df_title = self.df

            new = df_title["Title"].str.split(',"description"', n=1, expand=True)
            df_title["Title"] = new[0]
            df_title["Title_to_merge"] = new[0]
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).str.strip('"')
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).str.replace(' ', '_')
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).str.replace('-', '_')
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).str.replace(':', '')
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).str.replace('&', 'and')
            df_title["Title_to_merge"]  = df_title["Title_to_merge"].astype(str).str.lower()
            df_title["Title_to_merge"] = df_title["Title_to_merge"].astype(str).apply(unidecode)

            bad_titles = []

            pattern = '"ratingValue":(.*),"reviewCount"'

            df = pd.DataFrame()

            for title in df_title['Title_to_merge']:
                try:
                    r  =requests.get('https://www.rottentomatoes.com/m/'+title)
                    txt = r.text

                    soup = BeautifulSoup(txt, 'html.parser')
                    for gen in soup.find_all('script', {'type': "application/ld+json"}):
                        i = str(gen)
                        match = re.search(pattern, i).group(1)
                        temp_dict = [
                            {
                                'Title_to_merge': title,
                                'Rating': match,

                            }
                        ]
                        temp = pd.DataFrame.from_records(temp_dict)
                        df = pd.concat([df, temp])
                        temp.to_sql('RATINGS', self.engine, if_exists='append', index = False)

                except urllib.error.URLError:
                    print("Bad title")
                    bad_titles.append(title)
            with open('unidentified_titles.txt', 'w') as filehandle:
                for listitem in bad_titles:
                    filehandle.write('%s\n' % listitem)



            print("RATINGS have been updated")
            con.execute('drop table if exists TITLES_AND_RATINGS_OLD')

            con.execute('alter table if exists TITLES_AND_RATINGS rename to TITLES_AND_RATINGS_OLD')
            con.execute('create table TITLES_AND_RATINGS ( Code varchar not null, Title varchar, Title_to_merge varchar, Rating varchar)')

            joined = pd.merge(df_title,df, left_on='Title_to_merge', right_on='Title_to_merge')
            joined.to_sql('TITLES_AND_RATINGS', self.engine, if_exists='replace', index=False)
            return joined
