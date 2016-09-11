import tweepy
import os

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def tweetpunishment(eventname, dollaramount, charityname):
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : os.environ["CONSUMER_KEY"],
    "consumer_secret"     : os.environ["CONSUMER_SECRET"],
    "access_token"        : os.environ["ACCESS_TOKEN"],
    "access_token_secret" : os.environ["ACCESS_TOKEN_SECRET"]
    }

  api = get_api(cfg)
  tweet = "I was just late to " + eventname + " and had to donate "+ '${:,.2f}'.format(dollaramount) + " to " + charityname + "."
  status = api.update_status(status=tweet) 