'''
Write the script compute_pony_lang.py which is run as follows:
	python compute_pony_lang.py -c <pony_counts.json> -n <num_words>

The <pony_counts.json> file should have the same format output by your compile_word_counts.py script in Task 1.

It should compute the <num_words> for each pony that has the highest TF-IDF score. Note that to compute the inverse document frequency, you should use the number of times the words were used by all 6 ponies (i.e., only use the counts in the pony_counts.json, not all speakers from the original script).

The specific definition of TF-IDF you should implement is:
	tf-idf(w, pony, script) = tf(w, pony) x idf(w, script)
	tf(w, pony) = the number of times pony uses the word w (which we compute in task1)
	idf(w, script) = log [
		(total number of ponies) /
		(number of ponies that use the word w)
	]

Output should be written in JSON format to stdout with the following structure:
	{
		“<pony name>”: [ “highest-tfidf-word”, “second-highest-tfidf-word”, ... ],
		“<pony name>”: ...

Each pony word list should have <num_words> entries.

'''
import argparse
import json
import math
import os
from os.path import dirname, abspath

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--pony_counts', required=True)
    parser.add_argument('-n', '--num_words', required=True)
    args = parser.parse_args()
    
    return args.pony_counts, args.num_words

def get_tfidfs(all_word_counts):
    ponies = list(all_word_counts.keys())
    
    all_tfidfs = {}
    
    for pony in all_word_counts:
        all_tfidfs[pony] = {}
    
        for word in all_word_counts[pony]:
            # get tf
            tf = all_word_counts[pony][word]
            
            if tf <= 0:
                tfidf = 0
                
            else:
                # get idf
                num_ponies = len(all_word_counts)
                num_ponies_use_w = 0
                
                for p in ponies:
                    if all_word_counts[p][word] > 0:
                        num_ponies_use_w += 1
            
                tfidf = tf * math.log10(num_ponies / num_ponies_use_w)

            all_tfidfs[pony][word] = tfidf
            
    return all_tfidfs

def get_top_n_tfidfs(all_tfidfs, num_words):
    sorted_tfidfs = {}
    
    for pony in all_tfidfs:
        x = all_tfidfs[pony]
        sorted_tfidfs[pony] = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))
    
    top_n = {}
    
    for pony in sorted_tfidfs:
        sorted_keys = list(sorted_tfidfs[pony].keys())
        top_n[pony] = sorted_keys[:num_words]
    
    return top_n


def main():
    pony_counts, num_words = get_args()
    num_words = int(num_words)
    
    with open(pony_counts, 'r') as f:
        all_word_counts = json.load(f)
        
    all_tfidfs = get_tfidfs(all_word_counts)
    
    top_n_tfidfs = get_top_n_tfidfs(all_tfidfs, num_words)

    print(json.dumps(top_n_tfidfs, indent=4))
	

    
if __name__ == "__main__":
    main()
