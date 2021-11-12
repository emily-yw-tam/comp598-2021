'''
Write a script "collect_newest.py" that collects the 100 newest posts in the subreddit specified. It should run as follows:
	python3 collect_newest.py -o <output_file> -s <subreddit>

You should have exactly one post (in JSON format) per line.

'''
import argparse
import requests
import json
import os
from os.path import dirname, abspath

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output_file', required=True)
	parser.add_argument('-s', '--subreddit', required=True)
	args = parser.parse_args()

	return args.output_file, args.subreddit

def request_token():
	# request a token (https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example)
	client_auth = requests.auth.HTTPBasicAuth('RLzz7sTZZQNKqN-9a3mWNA', 'Kq5I2mSVr_1xAA49b5tkJP2XTZEHUA')
	post_data = {'grant_type': 'password', 'username': 'comp598-emily', 'password': 'Ilovecomp598!'}
	headers = {'User-Agent': 'PostCollectionBot/0.1 by comp598-emily'}
	res = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)
	token = res.json()['access_token']
	headers['Authorization'] = f'bearer {token}'

	return headers

# input: subreddit (e.g. '/r/mcgill'), headers from request_token()
# output: list of posts from subreddit
def collect_posts(subreddit, headers):
	r = requests.get(f'https://oauth.reddit.com{subreddit}/new?limit=100', headers=headers)
	root_element = r.json()
	posts_100 = root_element['data']['children']

	return posts_100

def store_data(posts, filename):
	# check if path exists
	currentdir = dirname(abspath(filename))
	if not os.path.exists(currentdir):
		os.makedirs(currentdir)

	print(f'Writing output to file {filename} ...')
	with open(filename, 'w') as f:
		for post in posts:
			f.write(json.dumps(post))
			f.write('\n')

	print('Done.')

def main():
	output_file, subreddit = get_args()
	headers = request_token()
	posts_100 = collect_posts(subreddit, headers)
	store_data(posts_100, output_file)



if __name__ == "__main__":
	main()

