'''
- Input file containing one JSON dict per line, corresponding to a subreddit post
- Output the average post title length
- In essence, it should accept one of the sample.json files produced by the collect.py script
- The input JSON dict should respect *exactly* the format returned by Reddit’s API
- The script is called like: python3 compute_title_lengths.py <input_file>

- If the post title doesn’t contain any text, it still counts as a post, just with text length of zero

'''
import json
import argparse

def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    filename = args.input_file

    sample_json = []    
    
    with open(filename, 'r') as f:
        input_lines = f.readlines()
        
    for line in input_lines:
        d = json.loads(line)
        sample_json.append(d)
    
    return sample_json

# input: list of json dictionaries
def get_titles(sample_json):
    titles = []
    
    for d in sample_json:
        title = d['data']['title']
        titles.append(title)
        
    return titles

# input: list of titles
def get_avg_length(titles):
    total_length = 0
    
    for title in titles:
        total_length += len(title)
        
    avg_length = total_length/len(titles)
    
    return avg_length

def main():
    sample_json = get_input()
    titles = get_titles(sample_json)
    avg_length = get_avg_length(titles)
        
    print(round(avg_length, 2))
    
    
    
if __name__ == "__main__":
    main()