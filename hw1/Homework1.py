import numpy as np
import pandas as pd

filename = 'https://github.com/fivethirtyeight/russian-troll-tweets/raw/master/IRAhandle_tweets_1.csv'

df = pd.read_csv(filename)

# first 10,000 tweets in the file
df10000 = df.iloc[:10000]

# tweets in English
# language = English
tweets_eng = df10000.loc[df10000['language'] == 'English']

print('Number of tweets that are in English:', tweets_eng.shape[0])

# tweets in English that don't contain a question
# content does not contain '?'
tweets_eng_nq = tweets_eng[~tweets_eng['content'].str.contains('?', regex=False)]

print('Number of tweets that are in English and don\'t contain a question:', tweets_eng_nq.shape[0])

# create tsv file
# tsv_file_1 = tweets_eng_nq.to_csv('data_collection.tsv', sep='\t', index=False)

trump_mention = tweets_eng_nq['content'].str.contains('\\bTrump\\b').values

tweets_eng_nq.insert(21, 'trump_mention', trump_mention)

# keep the following columns, in this order: tweet_id, publish_date, content, and  trump_mention
dataset = tweets_eng_nq[['tweet_id', 'publish_date', 'content', 'trump_mention']]

# create tsv file
# tsv_file_2 = dataset.to_csv('dataset.tsv', sep='\t', index=False)

# tweets that mention Trump
# trump_mention = True
num_trump = dataset.loc[dataset['trump_mention'] == True]

print('Number of tweets that mention Trump:', num_trump.shape[0])
print('Number of tweets that are in English and don\'t contain a question:', tweets_eng_nq.shape[0])

# % of tweets that mention Trump
value = num_trump.shape[0]/tweets_eng_nq.shape[0]
value_percent = value*100

print('Percent of tweets that mention Trump: %.3f' % value_percent)

d = {'result': ['frac-trump-mentions'], 'value': [value]}
results = pd.DataFrame(data=d)

# create tsv file
# tsv_file_3 = results.to_csv('results.tsv', sep='\t', index=False)
