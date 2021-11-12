'''
Write a script extract_to_tsv.py that accepts one of the files you collected from Reddit and outputs a random selection of posts from that file to a tsv (tab separated value) file. It should function like this:
	python3 extract_to_tsv.py -o <out_file> <json_file> <num_posts_to_output>

The output format (written to out_file) is:
	name <tab> title <tab> coding

- If <num_posts_to_output> is greater than the file length, then the script should just output all lines
- If there are more than <num_posts_to_output> (which is likely the case), then it should randomly select num_posts_to_output (the parameter you passed to the script) of them and just output those

'''
import argparse
import random
import json
import os
from os.path import dirname, abspath

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output_file', required=True)
	parser.add_argument('json_file')
	parser.add_argument('num_posts')
	args = parser.parse_args()

	try:
		num_posts = int(args.num_posts)
	except:
		num_posts = None

	return args.output_file, args.json_file, num_posts

def get_names_titles(json_file):
	names_titles = []
	
	with open(json_file, 'r') as f:
		input_lines = f.readlines()

	for line in input_lines:
		d = json.loads(line)
		name = d['data']['name']
		title = d['data']['title']
		names_titles.append((name, title))

	return names_titles

def get_random_selection(num_posts, names_titles):
	if num_posts >= len(names_titles):
		return names_titles
	else:
		random_selection = []
		indices = random.sample(range(len(names_titles)), num_posts)
		
		for i in indices:
			random_selection.append(names_titles[i])

		return random_selection

def main():
	# set random seed
	random.seed(1)

	# get arguments
	output_file, json_file, num_posts = get_args()
	
	if num_posts == None:
		print('Invalid <num_posts> value')
	
	else:
		# get all (names, titles) from posts
		all_names_titles = get_names_titles(json_file)

		# get random selection of posts
		random_selection = get_random_selection(num_posts, all_names_titles)

		# check if path exists
		currentdir = dirname(abspath(output_file))
		if not os.path.exists(currentdir):
			os.makedirs(currentdir)

		# output to tsv file
		with open(output_file, 'w') as f:
			f.write('Name\ttitle\tcoding\n')
			for post in random_selection:
				f.write(f'{post[0]}\t{post[1]}\t\n')



if __name__ == "__main__":
	main()
