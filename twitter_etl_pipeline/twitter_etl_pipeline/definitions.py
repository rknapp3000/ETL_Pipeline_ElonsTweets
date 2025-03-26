import dagster as dg
from .assets import twitter_client, raw_tweets, transformed_tweets, tweet_csv
from .jobs import twitter_etl_job
from .schedules import twitter_etl_schedule

# Define the assets
defs = dg.Definitions(
    assets=[twitter_client, raw_tweets, transformed_tweets, tweet_csv],
    jobs=[twitter_etl_job],
    schedules=[twitter_etl_schedule]
    )