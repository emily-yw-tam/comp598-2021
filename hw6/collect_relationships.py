'''
- Collects the relationships for a set of celebrities provided in a JSON configuration file as follows:
    python3 collect_relationships.py -c <config_file.json> -o <output_file.json>
- config_file.json contains a single JSON dictionary with the following structure (the exact path and list of celebrities can, obviously, change):
    {
        “cache_dir”: “data/wdw_cache”,
        “target_people”: [ “robert-downey-jr”, “justin-bieber” ]
    }

    In the configuration example above, we are targeting two people, "robert-downew-jr" and "justin-bieber", and we are caching their info under data/wdw_cache
- Your script will then go and fetch the relationships for the target individuals
- Note that the target people are indicated using the identifier that follows “/dating/”
- All pages visited MUST be cached in the cache directory specified – as described in the lecture
- This means that, if run twice on the same config file, it will use data exclusively from the cache the second time
- The output format for the file is:
    {
        “robert-downey-jr”: [ “person-1”, “person-2”, “person-3” ],
        “justin-bieber”: []
    }
- The identifiers in the list are the people the person had a relationship with
- If the person has had no relationships, then they will have an empty list

'''
import os
import argparse
import bs4
import json
import requests
import hashlib
import re
from os.path import dirname, abspath

# get arguments
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()

    return args.config_file, args.output_file

# get cache directory from config file
def get_cache_dir(config_file):
    with open(config_file, 'r') as f:
        d = json.load(f)
        cache_dir = d['cache_dir']
         
    return cache_dir

# get target people from config file
def get_target_people(config_file):
    with open(config_file, 'r') as f:
        d = json.load(f)
        target_people = d['target_people']
        
    return target_people

# get relationships for one person
# check the cache directory before fetching
def get_relationships(cache_dir, person):
    # generate sha1 hash of URL
    url = f'https://www.whosdatedwho.com/dating/{person}'
    cache_file = hashlib.sha1(url.encode('UTF-8')).hexdigest()
    
    # paths
    parentdir = dirname(dirname(abspath(__file__)))
    cache_dir_path = os.path.join(parentdir, cache_dir)
    cache_file_path = os.path.join(cache_dir_path, cache_file)
    
    # if a file named with hash string does not exist
    if not os.path.isfile(cache_file_path):
        # download url and save contents to file named with hash string
        print(f'Fetching {person} file...')
        page = requests.get(url)
        page.encoding = 'utf-8'
        with open(cache_file_path, 'wb') as f:
            f.write(page.content)
    else:
        print(f'Loading {person} file from cache...')
        
    soup = bs4.BeautifulSoup(open(cache_file_path, 'r'), 'html.parser', from_encoding='utf-8')
    
    # entire dating history is found under <div id="ff-dating-history-grid"...   
    grid_div = soup.find('div', id='ff-dating-history-grid')
    
    # name of each partner is found in <div class="ff-grid-box"...
    box_div = grid_div.find_all('div', class_='ff-grid-box')
    
    # within <div class="ff-grid-box", you will find id="dating-firstname-lastname(-optionaltag)"
    id_dating = re.findall(r'id="dating-[a-z]+[a-z\-]*"', str(box_div))
    
    relationships = []
    
    for p in id_dating:
        # slice knowing that string will always start with 'id="dating-' and end with '"'
        relationships.append(p[11:-1])    
    
    return relationships

def main():    
    config_file, output_file = get_args()
        
    cache_dir = get_cache_dir(config_file)
    target_people = get_target_people(config_file)
    
    output_dict = {}
        
    for person in target_people:
        output_dict[person] = get_relationships(cache_dir, person)
            
    with open(output_file, 'w') as f:
        json.dump(output_dict, f, indent=4)
    
    
    
if __name__ == "__main__":
    main()
