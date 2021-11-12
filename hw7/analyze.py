'''
Write a script called “analyze.py” which outputs the number of each category that appears in your annotated files. The script should run like this:
	python3 analyze.py -i <coded_file.tsv> [-o <output_file>]

The “-o …” argument is optional. If omitted, print the result to stdout. In either case, the output should be written in JSON format like this:
	{
	"course-related": 70,
	"food-related": 30,
	"residence-related": 20,
	"other": 80
	}

'''
import argparse
import json
import pandas as pd
import os
from os.path import dirname, abspath

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_file', required=True)
	parser.add_argument('-o', '--output_file')
	args = parser.parse_args()

	return args.input_file, args.output_file

def num_per_category(input_file, output_file, silent=True):
	df = pd.read_csv(input_file, sep='\t')
	categories = df['coding'].value_counts()

	d = {}

	if 'c' in categories:
		d['course-related'] = int(categories['c'])
	else:
		d['course-related'] = 0

	if 'f' in categories:
		d['food-related'] = int(categories['f'])
	else:
		d['food-related'] = 0

	if 'r' in categories:
		d['residence-related'] = int(categories['r'])
	else:
		d['residence-related'] = 0

	if 'o' in categories:
		d['other'] = int(categories['o'])
	else:
		d['other'] = 0

	if output_file != None:
		# check if path exists
		currentdir = dirname(abspath(output_file))

		if not os.path.exists(currentdir):
			os.makedirs(currentdir)

		with open(output_file, 'w') as f:
			json.dump(d, f, indent=0)

	else:
		silent = False

	if not silent:
		print('{')

		print(f'"course-related": {d["course-related"]},')
		print(f'"food-related": {d["food-related"]},')
		print(f'"residence-related": {d["residence-related"]},')
		print(f'"other": {d["other"]}')

		print('}')

def main():
	input_file, output_file = get_args()

	num_per_category(input_file, output_file)



if __name__ == "__main__":
	main()
