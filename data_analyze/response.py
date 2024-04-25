import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Function to get sentiment of a given text
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return 'positive', sentiment_score
    elif sentiment_score <= -0.05:
        return 'negative', sentiment_score
    else:
        return 'neutral', sentiment_score

# Load tweets from JSON file
def load_tweets_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading {filename}.")
        return []

# Sentiment analysis for each tweet
def analyze_tweets_sentiment(tweets):
    sorted_tweets = {'positive': [], 'negative': [], 'neutral': []}
    sentiment_scores = []

    for tweet in tweets:
        text = tweet.get('tweet_text', '')
        sentiment, sentiment_score = get_sentiment(text)
        sorted_tweets[sentiment].append({'tweet': text, 'sentiment_score': sentiment_score})
        sentiment_scores.append(sentiment_score)
    
    return sorted_tweets, sentiment_scores

# Print sentiment analysis results
def print_sentiment_analysis(sorted_tweets, sentiment_scores):
    print("Positive Tweets:")
    for tweet_data in sorted_tweets['positive']:
        print("-", tweet_data['tweet'], "Sentiment Score:", tweet_data['sentiment_score'])

    print("\nNegative Tweets:")
    for tweet_data in sorted_tweets['negative']:
        print("-", tweet_data['tweet'], "Sentiment Score:", tweet_data['sentiment_score'])

    print("\nNeutral Tweets:")
    for tweet_data in sorted_tweets['neutral']:
        print("-", tweet_data['tweet'], "Sentiment Score:", tweet_data['sentiment_score'])
    
    avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
    print("\nAverage Sentiment Score:", avg_sentiment_score)

# Set the JSON filename containing tweets
json_filename = input("Enter the JSON filename containing tweets: ")

# Load tweets from JSON file
tweets = load_tweets_from_json(json_filename)

# Analyze sentiment of tweets
sorted_tweets, sentiment_scores = analyze_tweets_sentiment(tweets)

# Print sentiment analysis results
print_sentiment_analysis(sorted_tweets, sentiment_scores)
