# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

import os

# these should definitely be environmental variables
customerId = '57d42deee63c5995587e8696'
apiKey = os.environ['APIKEY']

def createcustomer(first_name, last_name, street_number, street_name, city, state, zipcode):
    url = 'http://api.reimaginebanking.com/customers?{}'.format(apiKey)
    customer = {
        "first_name": first_name,
        "last_name": last_name,
        "address":{
            "street_number": str(street_number),
            "street_name": street_name,
            "city": city,
            "state": state,
            "zip": str(zipcode)
        }
    }
    print (json.dumps(customer))
    # now create the customer account
    response = requests.post(
        url,
        data=json.dumps(customer),
        headers={'content-type':'application/json', 'accept': 'application/json'},
        )
    if response.status_code == 400:
        print ("invalid input for customer")


    
def createaccount():
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
    print (response)
    if response.status_code == 201:
    	print('account created')