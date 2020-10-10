import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    
    def __init__(self):
        #keys and tokens from the Twiiter Dev Control
        consumer_key = "XJgFqi7mb2WytHBn5l6icbUMA"
        consumer_secret = "V6XBb6177TOZGJN86ZuGRKcmpGKhgEx0bpartBlvH1YACOArJA"
        access_token = "968160864489455616-T3mGvXRJyLYNJmZweIdYMJlWh0SLv85"
        access_token_secret = "wBllGLELcedBtdKk50BozhM3FXYg9I9OEoVHXfFyAjMS7"

        try:
            self.auth = OAuthHandler(consumer_key,consumer_secret)
            self.auth.set_access_token(access_token,access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error : Authentication Failed")
    
    def get_tweets(self,query,count=10):

        tweets = []
        try:
            fetched_tweets= self.api.search(q=query,count=count)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                    
                else:
                    tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as e:
            print("Error : "+ str(e))
