# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

import os

# these should definitely be environmental variables
customerId = '57d42deee63c5995587e8696'
apiKey = os.environ['APIKEY']

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Savings",
  "nickname": "test",
  "rewards": 10000,
  "balance": 10000,	
}
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print('account created')