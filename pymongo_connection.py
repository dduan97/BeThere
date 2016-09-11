#!/usr/bin/python

from pymongo import MongoClient

import os

# Your deployment's URI in the standard format (http://docs.mongodb.org/manual/reference/connection-string/).
#
# The URI can be found via the MongoLab management portal (http://docs.mongolab.com/connecting/#connect-string).
#

# Pass the following keyword arguments to ensure proper production behavior:
#
#   connectTimeoutMS  30 s to allow for PaaS warm-up; adjust down as needed for faster failures. For more, see docs:
#                     http://docs.mongolab.com/timeouts/#connection-timeout
#
#   socketTimeoutMS   No timeout (None) to allow for long-running operations
#                     (http://docs.mongolab.com/timeouts/#socket-timeout).
#
#   socketKeepAlive   Enabled (True) to ensure idle connections are kept alive in the presence of a firewall.
#
# See PyMongo docs for more details about the connection options:
#
#   https://api.mongodb.org/python/3.0/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient

mongolab_uri = os.environ["MONGO_URI"]

client = MongoClient(mongolab_uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)

db = client.get_default_database()
collection = db["bt_users"]

def createuser():
    user = {
                "name" : "Bill Clinton",
                "capital_one_ID" : "57d45391e63c5995587e86d9",
                "charity" : "World Wildlife Fund",
                "donated" : 5,
                "multiplier" : 1,
                "points" : 15
                
            }
    
    user_id = collection.insert_one(user).inserted_id

def getCharity():
    user = collection.find_one()
    return str(user["charity"])

# get the specified field, unsure which type
def getUserInfo(field):
    user = collection.find_one()
    return user[field]
    
# update field in user
def update(field, newvalue):
    result = collection.update_one(
            {'name' : 'Bill Clinton'},
            { '$set': {field: newvalue}}
    )
    print (result.matched_count)
