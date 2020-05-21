import pandas as pd
import urllib.request
import bs4 as bs
import re

class Movie_Titles:
    def __init__(self, movie_df, refresh_on_start, engine):
        self.df = movie_df
        self.refresh_on_start = refresh_on_start
        self.engine = engine

    def get_titles(self):
        """Obtain the titles of the movies in the movies dataframe.
        Outputs a dataframe with movie URLs and Title."""

        if self.refresh_on_start == True:
            con = self.engine.connect()
            con.execute('drop table if exists TITLES_OLD')

            con.execute('alter table if exists TITLES rename to TITLES_OLD')
            con.execute('create table TITLES ( Code varchar not null, Title varchar)')
            df = self.df
            movie_idx=df['Code'].unique()
            df_title = pd.DataFrame()
            pattern = '"name":(.*),"description"'

            for i in movie_idx:


                source = urllib.request.urlopen(i)
                soup = bs.BeautifulSoup(source, "html.parser")
                for gen in soup.find_all('script', {'type': "application/ld+json"}):
                    i_json = str(gen)
                    title = re.search(pattern, i_json).group(1)

                    temp_dict = [
                            {
                                'Code': i,
                                'Title': title,

                            }
                        ]
                    temp = pd.DataFrame.from_records(temp_dict)
                    temp.to_sql('TITLES', self.engine, if_exists='append', index = False)
                    df_title = pd.concat([df_title, temp])
            print("TITLES have been updated")

            return df_title
