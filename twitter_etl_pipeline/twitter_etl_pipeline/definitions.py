import dagster as dg
from .assets import twitter_client, raw_tweets, transformed_tweets, tweet_csv

# Define the assets
defs = dg.Definitions(assets=[twitter_client, raw_tweets, transformed_tweets, tweet_csv])