import bs4 as bs
import urllib.request
import requests
import pickle
from bs4 import BeautifulSoup
import pandas as pd
from rake_nltk import Metric, Rake
import spacy

class Scraped_Tags:
    def __init__(self, refresh_on_start, engine):
        self.refresh_on_start = refresh_on_start
        self.engine = engine


    def scrape_and_tag(self):
        """Obtain list of movies URLs from Netflix movies home page,
        scrape each link (that corresponds to a movie) to obtain the description of the movie,
        identify tags from the description using Rake.
        The Netflix genre tags are also included in the tags.
        This class returns a df that contains Code (movie URL) and Tags (obtained from movie description+Netflix tags).
        Dump the identified tags in a pickled file.
        The pickled file will make the comparison between tags and word in input much faster."""
        if self.refresh_on_start == True:
            con = self.engine.connect()
            con.execute('drop table if exists TAGS_OLD')

            con.execute('alter table if exists TAGS rename to TAGS_OLD')

            con.execute('create table TAGS ( Code varchar not null, Tags varchar)')

            resp = requests.get('https://www.netflix.com/browse/genre/34399')
            txt = resp.text
            soup = BeautifulSoup(txt, 'html.parser')
            df = pd.DataFrame()


            r_noStopWords = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,
                                 punctuations=',()’"?!,"-.')  # Uses stopwords for english from NLTK, and all puntuation characters.
            bad_links = []
            for a in soup.find_all('a', {'class': "nm-collections-title nm-collections-link"}):
                url = a['href']
                print("Requesting: ", url)
                try:
                    source = urllib.request.urlopen(url)
                    soup = bs.BeautifulSoup(source, "html.parser")

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
                            temp.to_sql('TAGS', self.engine, if_exists='append', index = False)

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
                        temp.to_sql('TAGS', self.engine, if_exists='append', index = False)

                        df = pd.concat([df, temp])





                except urllib.error.URLError:
                    print("Bad Link")
                    bad_links.append(url)
                with open('unidentified_links.txt', 'w') as filehandle:
                    for listitem in bad_links:
                        filehandle.write('%s\n' % listitem)

            nlp = spacy.load("en_core_web_lg")

            doc_list = {}
            idx = 0
            for i in df.Tags:
                idx = idx + 1
                doc_list[idx] = nlp(i)

            pfile = open("filename.pickle", 'wb')
            pickle.dump(doc_list, pfile, protocol=pickle.HIGHEST_PROTOCOL)
            pfile.close()
            print("TAGS have been updated and pickled")

            return df
