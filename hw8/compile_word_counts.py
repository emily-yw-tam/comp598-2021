'''
Write a script that computes word counts for each pony from all episodes of MLP.

Your script, compile_word_counts.py should run as follows:
	python compile_word_counts.py -o <word_counts_json> -d <clean_dialog.csv file>

The output file should be a dictionary with the following form:
	{
		“twilight sparkle”: {
			“<word1>”: <# of times the word1 is used by twilight sparkle>,
			“<word2>”: <# of times the word2 is used by twilight sparkle>,
			...
		},
		“pinkie pie”: {
			...
		}
		...
	}

Make sure you have exactly the following keys for the pony names: "twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy".

For your analysis:
- You should only keep words with a frequency higher than a specific threshold. For this homework, only keep words that occur at least 5 times across ALL valid speech acts.
- Remove all the stopwords.
- Only consider speech acts where the speaker is an exact match for one of the main character ponies. Ignore any others. Also lines which involve multiple characters, i.e. "Twilight and Fluttershy" or inexact matches, such as “future Twilight Sparkle” should be ignored.
- Treat each word encountered as case insensitive. Store words in all lowercase form.
- Before processing text, replace punctuation characters with a space. A punctuation character is one of these: ( ) [ ] , - . ? ! : ; # &
- A word must only include alphabetic characters. All other words should be ignored.
- Tip: to keep your script performant, store your word counts in dictionaries

'''
import argparse
import pandas as pd
import json
import os
from os.path import dirname, abspath

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file', required=True)
    parser.add_argument('-d', '--dialog_file', required=True)
    args = parser.parse_args()
    
    return args.output_file, args.dialog_file

# ponies = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
# punc = '()[],-.?!:;#&'
def get_dialog(dialog_file, ponies, punc):
    df = pd.read_csv(dialog_file)
    
    # only keep valid speech acts
    df['pony'] = df['pony'].str.lower()
    df = df.loc[df['pony'].isin(ponies)]
        
    # lowercase words, replace punctuation with spaces, split by spaces
    df['dialog'] = df['dialog'].str.lower()
    punc_to_space = str.maketrans(punc, ' ' * 13)
    df['dialog'] = df['dialog'].str.translate(punc_to_space)
    df['dialog'] = df['dialog'].str.split()
    
    return df

# get words that occur at least 5 times across ALL valid speech acts
def get_words(df, stopwords_file, frequency=5):
    # list of stopwords
    with open(stopwords_file) as f:
        stopwords = f.read().splitlines()[6:]
    
    all_words = {}
    
    dialog_list = df['dialog'].to_list()
    
    for dialog in dialog_list:
        for word in dialog:
            if (word.isalpha()) and (word not in stopwords):
                if word in all_words:
                    all_words[word] += 1
                else:
                    all_words[word] = 1
                    
    word_list = []
    
    for word in all_words:
        if all_words[word] >= frequency:
            word_list.append(word)
            
    return word_list

# output dictionary has all words in word_list
# some word counts could be 0
def get_word_counts(df, word_list, pony):
    word_counts = {word:0 for word in word_list}
    
    df_pony = df.loc[df['pony'] == pony]
    dialog_list = df_pony['dialog'].to_list()
    
    for dialog in dialog_list:
        for word in dialog:
            if word in word_counts:
                word_counts[word] += 1
    
    return word_counts

def main():
    output_file, dialog_file = get_args()
    
    ponies = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    punc = '()[],-.?!:;#&'
    
    df = get_dialog(dialog_file, ponies, punc)
    
    parentdir = dirname(dirname(abspath(__file__)))
    stopwords_file = 'stopwords.txt'
    stopwords_path = os.path.join(parentdir, 'data', stopwords_file)
        
    word_list = get_words(df, stopwords_path, frequency=5)
    
    all_word_counts = {}
    
    for pony in ponies:
        all_word_counts[pony] = get_word_counts(df, word_list, pony)
        
    # check if output file path exists
    outputdir = dirname(abspath(output_file))
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        
    # output to JSON file
    with open(output_file, 'w') as f:
        json.dump(all_word_counts, f, indent=4)
    
    

if __name__ == "__main__":
    main()
