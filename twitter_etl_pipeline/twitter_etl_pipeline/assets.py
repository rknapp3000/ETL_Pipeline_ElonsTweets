import os
import logging
import tweepy
import pandas as pd
from dagster import asset, get_dagster_logger

logger = get_dagster_logger()

# Authenticate Twitter API
@asset
def twitter_client():
    """Authenticate with Twitter API v2 using Bearer Token."""
    try:
        client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))
        logger.info("Twitter API authentication successful")
        return client
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        raise

# Fetch Tweets from Twitter
@asset(deps=[twitter_client])
def raw_tweets(twitter_client):
    """Fetch tweets using Twitter API v2."""
    try:
        username = "mattrife"
        user = twitter_client.get_user(username=username, user_auth=False)
        user_id = user.data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, 
            max_results=100, 
            tweet_fields=["created_at", "public_metrics"]
        )
        logger.info(f"Fetched {len(tweets.data)} tweets for {username}")
        return tweets.data if tweets.data else []
    except Exception as e:
        logger.error(f"Error fetching tweets: {e}")
        raise

# Transform Tweets into a structured format
@asset(deps=[raw_tweets])
def transformed_tweets(raw_tweets):
    """Extract relevant data from tweets."""
    extracted_data = []
    for tweet in raw_tweets:
        try:
            tweet_data = {
                "text": tweet.text,
                "created_at": tweet.created_at,
                "retweet_count": tweet.public_metrics["retweet_count"],
                "like_count": tweet.public_metrics["like_count"]
            }
            extracted_data.append(tweet_data)
        except Exception as e:
            logger.error(f"Error extracting tweet data: {e}")
            continue
    logger.info(f"Transformed {len(extracted_data)} tweets")
    return extracted_data

# Store Transformed Tweets into CSV
@asset(deps=[transformed_tweets])
def tweet_csv(transformed_tweets):
    """Save the structured tweet data to a CSV file."""
    try:
        df = pd.DataFrame(transformed_tweets)
        filename = "tweets.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Tweets saved to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
        raise
