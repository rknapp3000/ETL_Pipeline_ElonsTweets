import tweepy
import pandas as pd 
import os
import logging


def authenticate_twitter():
    """Authenticate with the Twitter API using credentials from environment variables."""
    try:
        auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
        auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
        api = tweepy.API(auth, wait_on_rate_limit=True)  # wait_on_rate_limit handles rate limiting
        return api
    except Exception as e:
        logging.error("Error during authentication: %s", e)
        raise


def fetch_tweets(api, username, tweet_count=200):
    """Fetch tweets from a given user timeline."""
    try:
        tweets = api.user_timeline(screen_name=username, 
                                   count=tweet_count,
                                   include_rts=False,
                                   tweet_mode='extended')
        return tweets
    except Exception as e:
        logging.error("Error fetching tweets: %s", e)
        raise


def extract_tweet_data(tweets):
    """Extract relevant data from tweets and return a list of dictionaries."""
    list_of_tweets = []
    for tweet in tweets:
        try:
            refined_tweet = {
                "user": tweet.user.screen_name,
                "text": tweet.full_text,  # Accessing full_text directly in tweet_mode='extended'
                "favorite_count": tweet.favorite_count,
                "retweet_count": tweet.retweet_count,
                "created_at": tweet.created_at
            }
            list_of_tweets.append(refined_tweet)
        except Exception as e:
            logging.error("Error extracting tweet data: %s", e)
            continue  # Skip tweet if there's any issue with it
    return list_of_tweets


def save_to_csv(tweet_data, filename='elons_tweets.csv'):
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
    
    # Authenticate and get API object
    api = authenticate_twitter()

    # Fetch tweets from Elon Musk's timeline
    tweets = fetch_tweets(api, username='elonmusk', tweet_count=200)

    # Extract tweet data and save to CSV
    tweet_data = extract_tweet_data(tweets)
    save_to_csv(tweet_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        run_twitter_etl()
    except Exception as e:
        logging.error("Error in ETL process: %s", e)
