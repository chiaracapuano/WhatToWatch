import pandas as pd
import urllib.request
import bs4 as bs
import re

class Movie_Titles:
    def __init__(self, movie_df):
        self.df = movie_df

    def get_titles(self):
        """Obtain the titles of the movies in the movies dataframe.
        Outputs a dataframe with movie URLs and Title."""

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
                df_title = pd.concat([df_title, temp])
        return df_title
