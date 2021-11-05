'''
- We’re going to try two different ways of sampling Reddit posts to assess their length:
    - Sample 1: Collect the 1000 newest posts from the 10 most popular subreddits by subscribers:
      funny, AskReddit, gaming, aww, pics, Music, science, worldnews, videos, todayilearned. This
      means you collect 100 posts from each
    - Sample 2: Collect the 1000 newest posts from the 10 most popular subreddits by # of posts by day:
      AskReddit, memes, politics, nfl, nba, wallstreetbets, teenagers, PublicFreakout, leagueoflegends, unpopularopinion.
      This means you collect 100 posts from each

- collect.py does the work of collecting the data for BOTH of the sampling approaches
- It stores the data (as received from Reddit) in files sample1.json and sample2.json (respectively)
- Reddit's API wraps posts into a key called "children", so sample1.json and sample2.json files must store the contents of the
children tag

- You are collecting POSTS, not comments (which are the responses to posts)
- To collect the posts you’ll want to use the /new API endpoint
- Make sure to set the User-Agent in your get requests...see API guidelines here: https://github.com/reddit-archive/reddit/wiki/API
- In order to get this data, you may need to authenticate to Reddit...instructions here: https://github.com/reddit-archive/reddit/wiki/OAuth2

'''
import requests
import json
import os
from os.path import dirname, abspath

def request_token():
    # request a token (https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example)
    client_auth = requests.auth.HTTPBasicAuth('RLzz7sTZZQNKqN-9a3mWNA', 'Kq5I2mSVr_1xAA49b5tkJP2XTZEHUA')
    post_data = {'grant_type': 'password', 'username': 'comp598-emily', 'password': 'Ilovecomp598!'}
    headers = {'User-Agent': 'PostCollectionBot/0.1 by comp598-emily'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)
    token = res.json()['access_token']
    headers['Authorization'] = f'bearer {token}'

    return headers

# input: list of subreddits, headers from request_token()
# output: list of posts from subreddits
def collect_posts(subreddits, headers):
    posts_1000 = []

    # loop through 10 most popular subreddits
    for subreddit in subreddits:
        # collect 100 posts from subreddit
        r = requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers)
        root_element = r.json()
        posts_100 = root_element['data']['children']
        posts_1000.append(posts_100)

    return posts_1000

# input: list of posts from subreddits, filename
# stores data in given filename
def store_data(posts, filename):
    # paths
    parentdir = dirname(dirname(abspath(__file__)))
    file_path = os.path.join(parentdir, filename)

    with open(file_path, 'w') as f:
        # loop through 10 subreddits
        for i in range(10):
			# loop through 100 posts from each subreddit
            for j in range(100):
                f.write(json.dumps(posts[i][j]))
                f.write('\n')

def main():
    # 10 most popular subreddits by subscribers
    sample1_sr = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']

    # 10 most popular subreddits by # of posts by day
    sample2_sr = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']

    headers = request_token()

    posts_1000_sub = collect_posts(sample1_sr, headers)
    posts_1000_pbd = collect_posts(sample2_sr, headers)
    
    store_data(posts_1000_sub, 'sample1.json')
    store_data(posts_1000_pbd, 'sample2.json')

    

if __name__ == "__main__":
    main()

