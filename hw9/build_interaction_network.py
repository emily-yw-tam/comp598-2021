'''
- In this assignment, we are modeling the interaction network as who speaks to who. 
- There is an (undirected) edge between two characters that speak to one another.
- The weight of the edge is how many times they speak to one another.
- We will say that character X speaks to character Y whenever character Y has a line IMMEDIATELY after character X in an episode.
- For consistency, lowercase all character names in the output JSON.

Keep the following in mind:
- A character can’t talk to itself.
- We’re considering the top 101 most frequent characters, not just the ponies.
- Don’t include characters that contain the following words in their names: “others”, “ponies”, "and", "all".
- Respect episode boundaries – interactions shouldn’t carry over.
- We are counting UNDIRECTED interactions – this means that if Spike speaks to Applejack and later Applejack speaks to Spike, then the number of interactions between them is 2.

Your script, build_interaction_network.py, should work as follows:
    python build_interaction_network.py -i /path/to/<script_input.csv> -o /path/to/<interaction_network.json>

'''
import pandas as pd
import argparse
import json
import re
import os
from os.path import dirname, abspath

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()
    
    return args.input_file, args.output_file

# get all episodes and top 101 most frequent characters
def get_chars(df):
    all_chars = df['pony'].value_counts().to_dict()
    
    keys = list(all_chars.keys())
    
    for key in keys:
        if re.search(r'\bothers\b|\bponies\b|\band\b|\ball\b', key) != None:
            all_chars.pop(key)
        
    sorted_chars = dict(sorted(all_chars.items(), key=lambda item:item[1], reverse=True))
    
    top_101_chars = list(sorted_chars.keys())[:101]

    return top_101_chars
                
def store_interactions(df, top_101_chars):
    interactions = {char:{} for char in top_101_chars}
    
    for row in df.itertuples():
        if getattr(row, 'Index') == 0:
            prev = (getattr(row, 'title'), getattr(row, 'pony'))
        elif getattr(row, 'Index') == (df.shape[0]-1):
            break
        else:
            curr = (getattr(row, 'title'), getattr(row, 'pony'))
            
            # check if episode is the same
            if prev[0] == curr[0]:
                if (prev[1] in top_101_chars) and (curr[1] in top_101_chars) and (prev[1] != curr[1]):
                    # add to first character
                    if curr[1] in interactions[prev[1]]:
                        interactions[prev[1]][curr[1]] += 1
                    else:
                        interactions[prev[1]][curr[1]] = 1
                    
                    # add to second character
                    if prev[1] in interactions[curr[1]]:
                        interactions[curr[1]][prev[1]] += 1
                    else:
                        interactions[curr[1]][prev[1]] = 1
            
            prev = (getattr(row, 'title'), getattr(row, 'pony'))
            
    return interactions

def main():
    input_file, output_file = get_args()
    
    df = pd.read_csv(input_file, usecols=['title', 'pony'])
    df['title'] = df['title'].str.lower()
    df['pony'] = df['pony'].str.lower()

    top_101_chars = get_chars(df)
    
    interactions = store_interactions(df, top_101_chars)
    
    # check if output file path exists
    outputdir = dirname(abspath(output_file))
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        
    # output to JSON file
    with open(output_file, 'w') as f:
        json.dump(interactions, f, indent=4)
    
    

if __name__ == "__main__":
    main()
