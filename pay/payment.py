import requests
import json

import os
import datetime

# charity account's id
charityId = '57d44dcbe63c5995587e86d5'
# user's id
userId = '57d42deee63c5995587e8696' 

# donation fund account ID
userAccountID = "57d45391e63c5995587e86d9"
apiKey = os.environ['APIKEY']


def addFunds(amount):
    url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(userAccountID,apiKey)
   
    deposit= {
      "medium": "balance",
      "transaction_date": str(datetime.datetime.today().date()),
      "amount": amount,
      "description": "nothing"
    }
    print(deposit)
    # Create a Savings Account
    response = requests.post( 
    	url, 
    	data=json.dumps(deposit),
    	headers={'content-type':'application/json'},
    	)
    print (response)
    if response.status_code == 201:
    	print('deposit added')

def donate(amount, charity_nickname):
    
    # find which ID to get by getting all accounts w/ id
    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(charityId,apiKey)
    
    response = requests.post (
        url,
        headers={'accept':'application/json'},
        )
    if response.status_code == 404:
        print("customer id does not exist")
    else:
        data = response.json()
        print(data)
    