'''
Write the script compute_network_stats.py which is run as follows:
    python compute_network_stats.py -i /path/to/<interaction_network.json> -o /path/to/<stats.json>
    
Using the networkx library, compute:
- The top three most connected characters by # of edges.
- The top three most connected characters by sum of the weight of edges.
    - Look at the sum total number of interactions the ponies had. 
    - Just check the inner keys for each pony in order to get the weights.
- The top three most central characters by betweenness.
    - Invoke betweenness_centrality in its simplest form (i.e. no need to specify weights nor other optional params).

Your output file should have structure:
    {
        “most_connected_by_num”: [c1, c2, c3],
        “most_connected_by_weight”: [c1, c2, c3],
        “most_central_by_betweenness”: [c1, c2, c3]
    }

'''
import networkx as nx
import argparse
import json
import os
from os.path import dirname, abspath

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()
    
    return args.input_file, args.output_file

def get_most_connected_by_num(G):
    degree_dict = dict(G.degree)
    sorted_dict = dict(sorted(degree_dict.items(), key=lambda item:item[1], reverse=True))
    
    top_3_by_num = list(sorted_dict.keys())[:3]
    
    return top_3_by_num

def get_most_connected_by_weight(G):
    degree_dict = dict(G.degree(weight='weight'))
    sorted_dict = dict(sorted(degree_dict.items(), key=lambda item:item[1], reverse=True))
    
    top_3_by_weight = list(sorted_dict.keys())[:3]
    
    return top_3_by_weight

def get_most_central(G):
    betweenness = nx.betweenness_centrality(G)
    sorted_dict = dict(sorted(betweenness.items(), key=lambda item:item[1], reverse=True))
    
    top_3_by_betweenness = list(sorted_dict.keys())[:3]
    
    return top_3_by_betweenness

def main():
    input_file, output_file = get_args()
    
    with open(input_file, 'r') as f:
        interactions = json.load(f)
        
    dod = {n1:{n2:{'weight':count} for n2, count in ndict.items()} for n1, ndict in interactions.items()}
 
    G = nx.from_dict_of_dicts(dod)
    
    stats = {}
    
    stats['most_connected_by_num'] = get_most_connected_by_num(G)
    stats['most_connected_by_weight'] = get_most_connected_by_weight(G)
    stats['most_central_by_betweenness'] = get_most_central(G)
    
    # check if output file path exists
    outputdir = dirname(abspath(output_file))
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        
    # output to JSON file
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=4)
    


if __name__ == "__main__":
    main()
