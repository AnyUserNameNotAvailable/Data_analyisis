import os
import scrapy
from scrapy.crawler import CrawlerProcess
import requests

def fetch_tweets(hashtag):
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    if not bearer_token:
        raise ValueError("Twitter Bearer Token not found.")

    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    params = {
        'q': f'#{hashtag}',  # Using hashtag in the search query
        'tweet_mode': 'extended',  # Ensures full text of tweets is returned
        'result_type': 'recent',   # Gets most recent tweets
        'count': 100               # Number of tweets to retrieve
    }

    url = 'https://api.twitter.com/2/tweets/search/recent'

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for unsuccessful responses

    data = response.json()

    tweets = []
    for tweet in data['data']:
        tweets.append(tweet['text'])

    return tweets

class TwitterScraper(scrapy.Spider):
    name = 'twitter_scraper'
    allowed_domains = ['api.twitter.com']
    
    def start_requests(self):
        hashtag = input("Enter the hashtag to search: ")

        # Fetch tweets using the Twitter API
        try:
            tweets = fetch_tweets(hashtag)
            for tweet in tweets:
                yield {'tweet_text': tweet}
        except Exception as e:
            print("An error occurred:", e)

# Running the spider
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'twitter_data.json'
})

process.crawl(TwitterScraper)
process.start()


# api key: LdQVXwDlL3slIkDjOyBFNq3iz
# Bearer Token: AAAAAAAAAAAAAAAAAAAAAPKLtQEAAAAAmwGSD1WXvBt4kxPdnmaQS99ZeLU%3DmpYtjA519oUjNQVgcf2QyY8pOsTdO7CFJKaVz5JEnx8K6D4GBa
# api key secrete: J0S6sXywF8ZzM27aROzFSDqcnnMkXOvXEkcCvpRMJlNIcjohvE