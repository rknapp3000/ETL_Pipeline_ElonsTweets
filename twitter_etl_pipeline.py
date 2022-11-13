import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 
import os
from dotenv import load_dotenv

def configure(): 
    load_dotenv()
    
def run_twitter_etl():
    configure()
    
    #Twitter authentication
    auth = tweepy.OAuthHandler(os.getenv(access_key), os.getenv(access_secret))   
    auth.set_access_token(os.getenv(consumer_key), os.getenv(consumer_secret)) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv('elons_tweets.csv')

# run_twitter_etl() used this method for testing 

