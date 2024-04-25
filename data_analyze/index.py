import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
import numpy as np

# Instantiate the TfidfVectorizer once, at the beginning of the file
tfidf_vectorizer = TfidfVectorizer(max_df=0.7)

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_from_json(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading {filename}.")
        return []

def index_hashtags_with_tfidf_to_json(hashtags, filename, tfidf_vectorizer):
    existing_data = read_from_json(filename)
    existing_hashtags = [doc['hashtags'] for doc in existing_data]
    all_hashtags = existing_hashtags + hashtags
    
    # Initialize existing_vectors as None
    existing_vectors = None

    # Fit the vectorizer on all hashtags if existing data is not empty, else fit on new hashtags only
    if existing_hashtags:
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_hashtags)
        existing_vectors = tfidf_matrix[:len(existing_hashtags)]
        new_vectors = tfidf_matrix[len(existing_hashtags):]
    else:
        new_vectors = tfidf_vectorizer.fit_transform(all_hashtags)
    
    for i, hashtag in enumerate(hashtags):
        if existing_vectors is not None:
            # Calculate cosine similarity between the new hashtag and existing ones
            similarity_scores = cosine_similarity(new_vectors[i], existing_vectors)
            
            # If any score exceeds the threshold, the hashtag is considered similar to an existing one
            if any(score[0] > 0.8 for score in similarity_scores):  # similarity_threshold = 0.8
                print(f"Similar hashtag detected: {hashtag}")
                continue
        
        # If the hashtag is not similar to existing ones, index it
        tfidf_values = new_vectors[i].toarray().flatten()
        index_hashtag_with_tfidf_to_json(hashtag, tfidf_values, filename)
        print(f"Indexed {hashtag} to JSON file")

    # Save the TF-IDF vectorizer to a file
    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')

def index_hashtag_with_tfidf_to_json(hashtag, tfidf_values, filename):
    doc = {
        'hashtag': hashtag,
        'tfidf_values': tfidf_values.tolist(),
    }
    existing_data = read_from_json(filename)
    existing_data.append(doc)
    write_to_json(existing_data, filename)

def run_crawler(start_url):
    crawled_items = []

    def crawler_results(item, response, spider):
        crawled_items.append(item)

    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler('crawlin')
    crawler.signals.connect(crawler_results, signal=signals.item_scraped)
    process.crawl(crawler, start_url=start_url)
    process.start()
    process.join()

    return crawled_items

# Set the JSON filename and website URL
json_filename = 'hashtags.json'
hashtag_texts = input('Enter hashtags separated by commas: ').split(',')

index_hashtags_with_tfidf_to_json(hashtag_texts, json_filename, tfidf_vectorizer)
