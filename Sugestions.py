import spacy
import warnings

warnings.filterwarnings("ignore")
from cachetools import cached


import pandas as pd
df_title = pd.read_csv(r'.\Movie_Titles.csv', encoding="utf-8")
new = df_title["Title"].str.split(',"description"', n = 1, expand = True)
df_title["Title"]= new[0]

nlp = spacy.load("en_core_web_lg")

##Import episodes+labels in dataframe
df = pd.read_csv(r'.\Netflix_Movies_All_Tags.csv', encoding="utf-8")
#df.drop_duplicates(inplace=True)

#input 
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
        df['Scores_1'] = 2*df['Scores_1']

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

joined = pd.merge(df_title,grouped, left_on='Code', right_on='Code')
top_suggestions = joined.sort_values('Scores_tot', ascending=False).head(5)

print(top_suggestions[['Title','Code']].to_string(index=False, header= False))
#output = top_suggestions[['Job','Podcast_Title_x','Episode_Title']]
#print(output)
#output.to_csv(r'C:\Users\adach\PycharmProjects\Podcasts_Scraping\Output.csv', index = False, mode='a', header =False)




