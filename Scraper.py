import bs4 as bs
import urllib.request
import requests
import pickle
from bs4 import BeautifulSoup
import pandas as pd
from rake_nltk import Metric, Rake
import spacy


class Scraped_Tags:

    def scrape_and_tag(self):
        """Obtain list of movies URLs from Netflix movies home page,
        scrape each link (that corresponds to a movie) to obtain the description of the movie,
        identify tags from the description using Rake.
        The Netflix genre tags are also included in the tags.
        This class returns a df that contains Code (movie URL) and Tags (obtained from movie description+Netflix tags).
        """

        resp = requests.get('https://www.netflix.com/browse/genre/34399')
        txt = resp.text
        soup = BeautifulSoup(txt, 'html.parser')
        df = pd.DataFrame()

        r_noStopWords = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,punctuations=',()’"?!,"-') # Uses stopwords for english from NLTK, and all puntuation characters.

        for a in soup.find_all('a', {'class': "nm-collections-title nm-collections-link"}):

            url = a['href']
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
        return df


    def pickle_tags(self):
        """Dump the identified tags in a pickled file.
        The pickled file will make the comparison between tags and word in input much faster."""

        nlp = spacy.load("en_core_web_lg")

        doc_list = {}
        idx = 0
        df = self.scrape_and_tag()
        for i in df.Tags:
            idx = idx+1
            doc_list[idx] = nlp(i)

        pfile = open("filename.pickle", 'wb')
        pickle.dump(doc_list, pfile, protocol=pickle.HIGHEST_PROTOCOL)
        pfile.close()
        return "Done pickling tags"