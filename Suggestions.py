import spacy
import warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")
import pickle
import pandas as pd
class Suggestions:

    def __init__(self, data_frame, data_frame_titles, input_word):
        self.word = input_word
        self.df = data_frame
        self.df_title = data_frame_titles

    import swifter



    def calculate_weigths(self):
        nlp = spacy.load("en_core_web_lg")


        def f_weights(row):
            if row['Scores_tot'] >= 0.5:
                val = 1
            else:
                val = 0.1
            return val

        if len(self.word) == 0:
            print("Empty word")
        else:
            count = 0
        doc_list = {}
        idx = 0

        for i in self.df.Tags:
            idx = idx + 1
            doc_list[idx] = nlp(i)
        pfile = open("filename.pickle", 'wb')
        pickle.dump(doc_list, pfile, protocol=pickle.HIGHEST_PROTOCOL)
        pfile.close()

        dbfile = open('filename.pickle', 'rb')
        db = pickle.load(dbfile)

        for i in self.word.split():
            count = count+1
            token_i = nlp(i)
            partial = []
            #self.df['Scores_'+str(i)] = self.df.swifter.apply(lambda x: get_similarity(x['Answer_'+str(i)], x['Tags']), axis=1)
            for key in db:
                partial.append(token_i.similarity(db[key]))

            self.df['Scores_' + str(count)] = partial
            self.df['Scores_1'] = 2*self.df['Scores_1']
            if 'Scores_2' in self.df.columns:
                self.df['Scores_2'] = 1.5 * self.df['Scores_2']
            else:
                self.df['Scores_NoSq_' + str(count)]= self.df['Scores_'+str(count)]
                self.df['Scores_' + str(count)] = self.df['Scores_' + str(count)].mul(self.df['Scores_' + str(count)]).mul(self.df['Scores_' + str(count)])
        dbfile.close()
        self.df['Scores_tot'] = 0

        for i in range(1, count+1):
            self.df['Scores_tot'] = self.df['Scores_tot'] + self.df['Scores_'+str(i)]

        self.df['Weights'] = self.df.apply(f_weights, axis=1)
        self.df['Scores_tot'] = self.df['Scores_tot'].mul(self.df['Weights'])
        return self.df


    def get_titles(self):
        new = self.df_title["Title"].str.split(',"description"', n=1, expand=True)
        self.df_title["Title"] = new[0]
        return self.df_title


    def display_results(self):
        df = self.calculate_weigths()
        df_title = self.get_titles()
        grouped = df.groupby(['Code']).mean().reset_index()
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        joined = pd.merge(df_title,grouped, left_on='Code', right_on='Code')
        print()
        top_suggestions = joined.sort_values('Scores_tot', ascending=False).head(5)
        return top_suggestions[['Title','Code', 'Rating']].to_string(index=False, header= False)


