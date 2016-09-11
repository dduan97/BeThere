import requests
import json

import os
import datetime

# charity account's id
charityAccount = '57d44dcbe63c5995587e86d5'
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
    if response.status_code == 201:
    	print('deposit added')

# nickname choices:
# American Bird Conservancy
# World Wildlife Fund
# Feeding America
def donate(amount, charity_nickname):
    
    # find which ID to get by getting all accounts w/ id
    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(charityAccount,apiKey)
    response = requests.get (
        url,
        headers={'accept':'application/json'},
        )
    if response.status_code != 200:
        print(response.status_code)
    else:
        data = response.json()
        charity_id = None
        for user in data:
            if charity_nickname == user["nickname"]:
                charity_id = user["_id"]
                break
    # if we know what to send money to, let's send the money
    if charity_id:
        url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(userAccountID, apiKey)
        transfer= {
            "medium": "balance",
            "payee_id": charity_id,
            "amount": amount,
            "transaction_date": str(datetime.datetime.today().date()),
            "description": "I was late and this is my punishment"
        }
        response = requests.post (
            url, 
            data = json.dumps(transfer),
            headers={'content-type':'application/json'},
            )
        if response.status_code != 201:
            print(response.status_code)
            return False
        # was successful, return true
        else:
            return True
        