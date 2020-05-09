import bs4 as bs
import urllib.request
import requests
r  =requests.get('https://www.netflix.com/title/81226439')
txt = r.text
import re
from bs4 import BeautifulSoup
soup = BeautifulSoup(txt, 'html.parser')
pattern = '"genre":(.*),"image"'
"""
for d in soup.find_all('script', {'type': "application/ld+json"}):
        print(str(d))
        i = str(d)
        match = re.search(pattern, i).group(1)

        print(match)
#print(soup)
"""
resp = requests.get('https://www.netflix.com/browse/genre/34399')
txt = resp.text
from bs4 import BeautifulSoup
soup = BeautifulSoup(txt, 'html.parser')
import pandas as pd
df = pd.DataFrame()
from rake_nltk import Metric, Rake

r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,punctuations=',()', stopwords='podcast') # Uses stopwords for english from NLTK, and all puntuation characters.
r_noStopWords = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,punctuations=',()’"?!,"-') # Uses stopwords for english from NLTK, and all puntuation characters.

for a in soup.find_all('a', {'class': "nm-collections-title nm-collections-link"}):

    url = a['href']
    source = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(source, "html.parser")
    for gen in soup.find_all('script', {'type': "application/ld+json"}):
        i = str(gen)
        match = re.search(pattern, i).group(1)

    for d in soup.find_all('div', {'class': "title-info-synopsis"}):
        i = d.text
        r_noStopWords.extract_keywords_from_text(i)
        rks_noStopWords = r_noStopWords.get_ranked_phrases()

        for wrd in rks_noStopWords:
            splitted = wrd.split()

            temp = pd.DataFrame(
                {
                    'Code': url,
                    'Tags': splitted
                }
            )

            df = pd.concat([df, temp])

    for elem in soup.findAll('span', {'class': 'more-details-item item-genres'}):
        genre = elem.text.replace(',', '')



        temp_dict = [
                {
                    'Code': url,
                    'Tags': genre,

                }
            ]
        temp = pd.DataFrame.from_records(temp_dict)
        df = pd.concat([df, temp])
df.to_csv(r'.\Netflix_Movies_All_Tags.csv', index=False)

