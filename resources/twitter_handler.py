


## initialize twitter api & login
import tweepy
from resources.config import settings_manager

settings = settings_manager()

class twitter_handler():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):

        self.consumer_key = settings.twitter_consumer_key
        self.consumer_secret = settings.twitter_consumer_secret
        self.access_token = settings.twitter_access_token
        self.access_token_secret = settings.twitter_access_token_secret

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



    ##### GET TWITTER USERNAME
    def get_twitter_username(self):
        return self.api.me().screen_name


    ##### GET TWITTER LINK
    def get_twitter_link(self):
        return self.api.me().url


    ##### CREATE NEW TWEETS
    def create_new_tweet(self, tweet_text):
        tweet = self.api.update_status(tweet_text)
        return tweet



    ##### GET TWEET ANALYTICS
    def get_tweet_analytics(self, tweet_id):
        tweet = self.api.get_status(tweet_id)
        return tweet


    
    def get_all_tweets(self):
        return self.api.user_timeline()