import spacy
import warnings

warnings.filterwarnings("ignore")
from cachetools import cached

nlp = spacy.load("en_core_web_lg")

import pandas as pd

##Import episodes+labels in dataframe
df = pd.read_csv(r'.\Netflix_Movies_Multiple_Tags.csv', encoding="utf-8")
df.drop_duplicates(inplace=True)

#input job/personality
word = input("Please enter a word: \n")

count = 0
print("The top 5 suggestions are:")
for i in word.split():
    count = count+1
    df['Answer_'+str(count)] = i


@cached(cache={})
def get_similarity(term1, term2):
    tokens = nlp(term1 + " " + term2)
    return tokens[0].similarity(tokens[1])



def f_weights(row):
    if row['Scores_tot'] >=0.5:
        val = 1
    else:
        val = 0.1
    return val

##Calculating similarity and weights
import swifter
def calculate_weigths(df):
    for i in range(1, count+1):
        df['Scores_'+str(i)] = df.swifter.apply(lambda x: get_similarity(x['Answer_'+str(i)], x['Tags']), axis=1)
        df['Scores_NoSq_' + str(i)]=df['Scores_'+str(i)]
        df['Scores_' + str(i)] = df['Scores_' + str(i)].mul(df['Scores_' + str(i)] ).mul(df['Scores_' + str(i)] )

    df['Scores_tot'] = 0

    for i in range(1, count+1):
        df['Scores_tot'] = df['Scores_tot'] + df['Scores_'+str(i)]

    df['Weights'] = df.apply(f_weights, axis=1)
    df['Scores_tot'] = df['Scores_tot'].mul(df['Weights'])
    return df

df = calculate_weigths(df)
grouped = df.groupby(['Code']).mean().reset_index()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
#df_title = pd.read_csv(r'C:\Users\adach\PycharmProjects\Podcasts_Scraping\Podcast_list_assignment_titles.csv', encoding="utf-8")
#joined = pd.merge(df,grouped, left_on='Code', right_on='Podcast_Title')
top_3_suggestions = grouped.sort_values('Scores_tot', ascending=False).head(5)

print(top_3_suggestions[['Code']].to_string(index=False, header= False))
#top_3_suggestions['Job'] = word
#output = top_3_suggestions[['Job','Podcast_Title_x','Episode_Title']]
#print(output)
#output.to_csv(r'C:\Users\adach\PycharmProjects\Podcasts_Scraping\Output.csv', index = False, mode='a', header =False)




