# computes and produces a JSON-formatted result that has exactly the structure given in the Homework 3 instructions

# script should run as follows:
# python3 dialog_analysis.py -o output.json clean_dialog.csv

import argparse
import pandas as pd
import json

parser = argparse.ArgumentParser()
parser.add_argument('-o')
parser.add_argument('dialog')
args = parser.parse_args()

filename = args.dialog

df = pd.read_csv(filename)

# convert all pony names to lowercase
df['pony'] = df['pony'].str.lower()

twilight_sparkle = df.loc[df['pony'] == 'twilight sparkle']
applejack = df.loc[df['pony'] == 'applejack']
rarity = df.loc[df['pony'] == 'rarity']
pinkie_pie = df.loc[df['pony'] == 'pinkie pie']
rainbow_dash = df.loc[df['pony'] == 'rainbow dash']
fluttershy = df.loc[df['pony'] == 'fluttershy']

# count shows the number of speech acts that each character has in the entire file
count = {}
count['twilight sparkle'] = twilight_sparkle.shape[0]
count['applejack'] = applejack.shape[0]
count['rarity'] = rarity.shape[0]
count['pinkie pie'] = pinkie_pie.shape[0]
count['rainbow dash'] = rainbow_dash.shape[0]
count['fluttershy'] = fluttershy.shape[0]

# verbosity gives the fraction of dialogue, measured in # of speech acts produced by this pony
# only want to see the values related to the six ponies (the main characters of the cartoon)
total = df.shape[0]

verbosity = {}
verbosity['twilight sparkle'] = round(twilight_sparkle.shape[0]/total, 2)
verbosity['applejack'] = round(applejack.shape[0]/total, 2)
verbosity['rarity'] = round(rarity.shape[0]/total, 2)
verbosity['pinkie pie'] = round(pinkie_pie.shape[0]/total, 2)
verbosity['rainbow dash'] = round(rainbow_dash.shape[0]/total, 2)
verbosity['fluttershy'] = round(fluttershy.shape[0]/total, 2)

# write to JSON file
if args.o is None:
    output_file = 'output.json'
else:
    output_file = args.o

count_verbosity = {}
count_verbosity['count'] = count
count_verbosity['verbosity'] = verbosity

with open(output_file, 'w') as json_file:
    json.dump(count_verbosity, json_file, indent=2)


