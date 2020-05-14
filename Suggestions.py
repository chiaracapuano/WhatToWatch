import warnings
warnings.filterwarnings("ignore")
import pandas as pd




class Suggestions:
    def __init__(self, data_frame, data_frame_titles, input_word, file, nlp):
        self.word = input_word
        self.df = data_frame
        self.df_title = data_frame_titles
        self.db = file
        self.nlp = nlp

    def calculate_weigths(self):
        """Compares movies tags with user input word.
        Tags are contained in picked file given as class argument."""

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

        for i in self.word.split():
            count = count+1

            token_i = self.nlp(i)

            partial = []
            for key in self.db:
                partial.append(token_i.similarity(self.db[key]))
            print(len(partial))
            self.df['Scores_' + str(count)] = partial
            self.df['Scores_1'] = 2*self.df['Scores_1']
            if 'Scores_2' in self.df.columns:
                self.df['Scores_2'] = 1.5 * self.df['Scores_2']
            else:
                self.df['Scores_NoSq_' + str(count)]= self.df['Scores_'+str(count)]
                self.df['Scores_' + str(count)] = self.df['Scores_' + str(count)].mul(self.df['Scores_' + str(count)]).mul(self.df['Scores_' + str(count)])

        self.df['Scores_tot'] = 0

        for i in range(1, count+1):
            self.df['Scores_tot'] = self.df['Scores_tot'] + self.df['Scores_'+str(i)]

        self.df['Weights'] = self.df.apply(f_weights, axis=1)
        self.df['Scores_tot'] = self.df['Scores_tot'].mul(self.df['Weights'])

        df_title = self.df_title
        grouped = self.df.groupby(['Code']).mean().reset_index()
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        joined = pd.merge(df_title,grouped, left_on='Code', right_on='Code')
        top_suggestions = joined.sort_values('Scores_tot', ascending=False).head(5)
        return top_suggestions[['Title','Code', 'Rating']].to_string(index=False, header= False)


