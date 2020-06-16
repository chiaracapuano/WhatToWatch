import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from jinja2 import Environment, FileSystemLoader


class Suggestions:
    def __init__(self, data_frame, data_frame_titles, input_word, file, nlp):
        self.word = input_word
        self.df = data_frame
        self.df_titles_and_ratings = data_frame_titles
        self.db = file
        self.nlp = nlp

    def calculate_weigths(self):
        """Compares movies tags with user input word. A semantic similarity score is obtained.
        Tags are contained in picked file given as class argument.
        The score is cubed to "punish" low scores and enhance high scores.
        If there is more than a word in input, the first one's scores are multiplied by 2,
        the second input word scores multiplied by 1.5.
        The HTML code for rendering the dataframe is contained in ./templetes/output.html
        """


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

            self.df['Scores_' + str(count)] = partial

            self.df['Scores_' + str(count)] = self.df['Scores_' + str(count)].\
                mul(self.df['Scores_' + str(count)]).\
                mul(self.df['Scores_' + str(count)])

            self.df['Scores_1'] = 2*self.df['Scores_1']

            if 'Scores_2' in self.df.columns:
                self.df['Scores_2'] = 1.5 * self.df['Scores_2']


        self.df['Scores_tot'] = 0

        for i in range(1, count+1):
            self.df['Scores_tot'] = self.df['Scores_tot'] + self.df['Scores_'+str(i)]


        df_titles_and_ratings = self.df_titles_and_ratings
        grouped = self.df.groupby(['Code']).mean().reset_index()
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 400)
        pd.set_option('display.max_colwidth', None)
        joined = pd.merge(df_titles_and_ratings, grouped, left_on='Code', right_on='Code')
        top_suggestions = joined.sort_values('Scores_tot', ascending=False).head(5)
        top_suggestions.rename(columns={'Code': 'Link'}, inplace = True)
        top_suggestions.fillna(value='Tomatometer not available', inplace=True)
        top_suggestions["Rating"] = top_suggestions["Rating"].replace('null', 'Tomatometer not available')

        env = Environment(loader=FileSystemLoader('./templates'))

        template = env.get_template("output.html")

        template_vars = {"top_suggestions": top_suggestions[['Title','Link', 'Rating']].to_html(index=False, escape=False, render_links = True)}
        return template.render(template_vars)
