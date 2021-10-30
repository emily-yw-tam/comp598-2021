'''
Clean up messy JSON entries.

Accepts an input file and produces a cleaned output file:
    python3 clean.py -i <input_file> -o <output_file>
    
1. Remove all the posts that don’t have either a title or title_text field.
2. For objects with a title_text field, rename the field in the output object to title.
3. Standardize all createdAt date times to the UTC timezone.
4. Remove all the posts with invalid date time that can’t be parsed using the ISO datetime standard.
5. Remove all the posts that are invalid JSON dictionaries.
6. Remove all the posts where the author field is empty, null, or N/A.
7. The value in the total_count can only be type int, float, str. You must attempt to cast float and str to an int value. 
   Some examples:
    
    "3" -> 3; "27" -> 27
    "twenty" -> INVALID
    22.1 -> 22; 22.9 -> 22
    
    If you are unable to cast total_count to int, remove the post.
8. Remove all posts if the type of total_count is anything other than int, float, str. If total_count is not present, 
   you do not have to remove the JSON object; keep it in the output file.
9. The tags field should be a list of individual words (where each word does NOT contain a space). 
   Any element that contains spaces should be split into separate words. If the tags field is not present, 
   you do not have to drop the record; keep the record in the output file. In the input files we'll use, 
   tags will always be a list. Do not worry about conversions.

    e.g. if tags is ['golf', 'tennis', 'football games'], after processing it should be ['golf', 'tennis', 'football', 'games']

10. Posts that haven’t been flagged for removal should be written to the output file in the order they appear in the input file.

'''

import argparse
import json
from datetime import datetime, timezone

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file')
    args = parser.parse_args()
    
    input_name = args.input_file
    output_name = args.output_file
    
    if output_name == None:
        output_name = 'output_file.txt'
    
    return input_name, output_name

# 5: remove posts that are invalid JSON dicts
def clean_invalid(line):
    try:
        d = json.loads(line)
        return d
    except:
        return None

# 1: ignore dicts that don't have 'title' or 'title_text' key
# 2: replace 'title_text' key with 'title'
def clean_title(d):
    if 'title' in d:
        return d
    elif 'title_text' in d:
        d['title'] = d.pop('title_text')
        return d
    else:
        return None
        
# 3: if 'createdAt' key exists, standardize date times to UTC timezone
# 4: ignore dicts that have invalid date time
def clean_date(d):
    if 'createdAt' in d:
        try:
            iso = datetime.strptime(d['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
            d['createdAt'] = iso.astimezone(timezone.utc).isoformat() 
            return d
        except:
            return None
    else:
        return d

# 6: ignore posts where author field is empty, null, or N/A
def clean_author(d):
    if 'author' in d:
        invalid_list = ['', 'null', 'n/a']

        if d['author'] == None:                     # is None
            return None
        
        elif not isinstance(d['author'], str):      # not a string
            return None
        
        elif d['author'].lower() in invalid_list:   # is empty, null, or N/A
            return None
        
        else:
            return d
    else:
        return d
            
# 8: ignore dicts that have 'total_count' value of type that is not int, float, or str
# 7: cast 'total_count' value to int if it is a float or str
def clean_total_count(d):
    if 'total_count' in d:
        if d['total_count'] == None:                                                        # is None
            return None
        
        elif isinstance(d['total_count'], int):                                             # is type int
            return d
        
        elif isinstance(d['total_count'], float) or isinstance(d['total_count'], str):      # is type float or str
            try:
                d['total_count'] = int(d['total_count'])
                return d
            except:
                return None
            
        else:                                                                               # not type int, float, or str
            return None
        
    else:
        return d
   
# assumption: tags will always be a list
# 9: split tags list elements that contain spaces
def clean_tags(d):
    if 'tags' in d:
        to_remove = []
        to_append = []
        
        for word in d['tags']:
            if isinstance(word, str):
                if ' ' in word:
                    split_string = word.split()
                    for s in split_string:
                        to_append.append(s)
                    to_remove.append(word)
        
        for r in to_remove:
            d['tags'].remove(r)
            
        for a in to_append:
            d['tags'].append(a)
            
        return d
                    
    else:
        return d

def clean_dict(d):
    if d == None:
        return None
    
    d = clean_title(d)
    if d == None:
        return None
    
    d = clean_date(d)
    if d == None:
        return None
    
    d = clean_author(d)
    if d == None:
        return None
    
    d = clean_total_count(d)
    if d == None:
        return None
    
    d = clean_tags(d)
    if d == None:
        return None
    
    return d

def main():
    input_name, output_name = get_args()
        
    with open(input_name, 'r') as file:
        input_lines = file.readlines()

    input_dicts = []
    
    # 5: remove posts that are invalid JSON dicts
    for line in input_lines:
        d = clean_invalid(line)
        if d != None:
            input_dicts.append(d)
        
    output_dicts = []
    
    for d in input_dicts:
        cleaned_d = clean_dict(d)
        
        if cleaned_d != None:
            output_dicts.append(cleaned_d)
            
    # write cleaned dicts to output file in the order they appear in the input file
    with open(output_name, 'w') as file:
        file.write('\n'.join(json.dumps(d) for d in output_dicts))

if __name__ == "__main__":
    main()
