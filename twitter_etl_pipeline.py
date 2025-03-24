import tweepy
import pandas as pd
import os
import logging

def authenticate_twitter():
    """Authenticate with Twitter API v2 using Bearer Token."""
    try:
        client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))
        return client
    except Exception as e:
        logging.error("Error during authentication: %s", e)
        raise

def fetch_tweets(client, username, tweet_count=100):
    """Fetch tweets using Twitter API v2."""
    try:
        user = client.get_user(username=username, user_auth=False)
        user_id = user.data.id
        tweets = client.get_users_tweets(
            id=user_id, 
            max_results=tweet_count, 
            tweet_fields=["created_at", "public_metrics"]
        )
        return tweets.data if tweets.data else []
    except Exception as e:
        logging.error("Error fetching tweets: %s", e)
        raise

def extract_tweet_data(tweets):
    """Extract relevant data from tweets."""
    list_of_tweets = []
    for tweet in tweets:
        try:
            refined_tweet = {
                "text": tweet.text,
                "created_at": tweet.created_at,
                "retweet_count": tweet.public_metrics["retweet_count"],
                "like_count": tweet.public_metrics["like_count"]
            }
            list_of_tweets.append(refined_tweet)
        except Exception as e:
            logging.error("Error extracting tweet data: %s", e)
            continue
    return list_of_tweets

def save_to_csv(tweet_data, filename='tweets.csv'):
    """Save the tweet data to a CSV file."""
    try:
        df = pd.DataFrame(tweet_data)
        df.to_csv(filename, index=False)
        logging.info("Tweets saved to %s", filename)
    except Exception as e:
        logging.error("Error saving to CSV: %s", e)
        raise

def run_twitter_etl():
    """Main function to run the Twitter ETL process."""
    client = authenticate_twitter()
    tweets = fetch_tweets(client, username="mattrife", tweet_count=100)
    tweet_data = extract_tweet_data(tweets)
    save_to_csv(tweet_data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        run_twitter_etl()
    except Exception as e:
        logging.error("Error in ETL process: %s", e)
