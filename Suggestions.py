import spacy
import warnings

warnings.filterwarnings("ignore")
from cachetools import cached


import pandas as pd
class Suggestions:
    #    df = pd.read_csv(r'./Netflix_Movies_All_Tags.csv', encoding="utf-8")

    def __init__(self, data_frame, data_frame_titles, input_word):
        self.word = input_word
        self.df = data_frame
        self.df_title = data_frame_titles





    ##Import episodes+labels in dataframe
    #df.drop_duplicates(inplace=True)

    #input
    #word = input("Please enter a word: \n")

    count = 0
    #print("The top 5 suggestions are:")



    @cached(cache={})
    def get_similarity(self, term1, term2):
        nlp = spacy.load("en_core_web_lg")
        tokens = nlp(term1 + " " + term2)

        return tokens[0].similarity(tokens[1])



    def f_weights(self, row):
        if row['Scores_tot'] >=0.5:
            val = 1
        else:
            val = 0.1
        return val

    ##Calculating similarity and weights
    import swifter
    def calculate_weigths(self):
        for i in self.word.split():
            count = count+1
            self.df['Answer_'+str(count)] = i

        for i in range(1, count+1):
            self.df['Scores_'+str(i)] = self.df.swifter.apply(lambda x: self.get_similarity(x['Answer_'+str(i)], x['Tags']), axis=1)
            self.df['Scores_1'] = 2*self.df['Scores_1']
            self.df['Scores_2'] = 1.5 * self.df['Scores_2']
            self.df['Scores_NoSq_' + str(i)]= self.df['Scores_'+str(i)]
            self.df['Scores_' + str(i)] = self.df['Scores_' + str(i)].mul(self.df['Scores_' + str(i)] ).mul(self.df['Scores_' + str(i)] )

        self.df['Scores_tot'] = 0

        for i in range(1, count+1):
            self.df['Scores_tot'] = self.df['Scores_tot'] + self.df['Scores_'+str(i)]

        self.df['Weights'] = self.df.apply(self.f_weights, axis=1)
        self.df['Scores_tot'] = self.df['Scores_tot'].mul(self.df['Weights'])
        return self.df

   # df = calculate_weigths(df)
    def get_titles(self):
        new = self.df_title["Title"].str.split(',"description"', n=1, expand=True)
        self.df_title["Title"] = new[0]
        return self.df_title

    def display_results(self):
        df = self.calculate_weigths()
        df_title = self.get_titles()
        #df_title = pd.read_csv(r'./Movie_Titles.csv', encoding="utf-8")

        grouped = df.groupby(['Code']).mean().reset_index()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        joined = pd.merge(df_title,grouped, left_on='Code', right_on='Code')
        top_suggestions = joined.sort_values('Scores_tot', ascending=False).head(5)

        return print(top_suggestions[['Title','Code']].to_string(index=False, header= False))
    #output = top_suggestions[['Job','Podcast_Title_x','Episode_Title']]
    #print(output)
    #output.to_csv(r'C:\Users\adach\PycharmProjects\Podcasts_Scraping\Output.csv', index = False, mode='a', header =False)




