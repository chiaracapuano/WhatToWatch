import pandas as pd
df = pd.read_csv(r'.\Netflix_Movies_Multiple_Tags.csv', encoding="utf-8")

movie_idx=df['Code'].unique()
import urllib.request
import bs4 as bs
df_title = pd.DataFrame()
import re
pattern = '"name":(.*),"description"'
#pattern2 = '"genre":(.*),"image"'

for i in movie_idx:
    #print("idx",i)

    source = urllib.request.urlopen('https://www.netflix.com/title/70209245')
    soup = bs.BeautifulSoup(source, "html.parser")
    #print(soup)
    for gen in soup.find_all('script', {'type': "application/ld+json"}):
        i_json = str(gen)
        title = re.search(pattern, i_json).group(1)
        #genre = re.search(pattern2, i_json).group(1)
        #span class="more-details-item item-genres" data-uia="more-details-item-genres">
    for elem in soup.findAll('span', {'class': 'more-details-item item-genres'}):
        genre = elem.text.replace(',', '')

        #print(title)
        #print(genre)

        temp_dict = [
                {
                    'Code': i,
                    'Title': title,
                    'Netflix_Tag': genre,

                }
            ]
        temp = pd.DataFrame.from_records(temp_dict)
        df_title = pd.concat([df_title, temp])
    #print(df_title)

df_title.to_csv(r'.\Movie_Titles.csv', index = False)
