import datetime
from flask import Flask, request
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from my_calendar import get_events
from event_lock import EventLock, OneEventToRuleThemAll
import json
app = Flask(__name__)

import os

@app.route("/")
def hello():
    return "Hello World!"

# post a location for an event when it gets to the time
# request should have fields:
# {
#   latitude: float
#   longitude: float
# }
# request.args for url query parameters
@app.route("/event/<event_id>/location", methods=['POST'])
def check_location(event_id):

    lat = request.args.get("latitude")
    lon = request.args.get("longitude")
    print lat,lon

    # now we set the lock and get the event thing based on the whatever
    EventLock.acquire()
    coords = OneEventToRuleThemAll.get_location_by_event_id(event_id)
    EventLock.release()
    if not coords:
        return "None"

    event_coords = (coords["latitude"], coords["longitude"])
    current_coords = (float(lat), float(lon))

    if vincenty(event_coords, current_coords).feet < 100:
        return "true"
    return "false"

# post a new charity/money amount configuration
# request:
# {
#   username: string
#   amount: float  
# }
@app.route("/payment", methods=['POST'])
def send_payment():
    # pass it off to the payment thing here
    pass

def get_event_info():
    events = get_events()
    current = datetime.datetime.now()
    # list of (id, name, datetime) for all the events
    event_ids_times = map(lambda x: {
            "id": x["id"], 
            "name": x["summary"], 
            "start_time": x["start"]["dateTime"][:-6],
            "recurring_event_color": x["recurring_event_color"] if "recurringEventID" in events else None,
            "location": x["location"] if "location" in x.keys() else "1350 Chestnut Street, Philadelphia, PA, United States"
        }, events)
    return event_ids_times

# route to retrieve events for the next week
# response:
# 
@app.route("/events", methods=['GET'])
def send_events():
    event_info = get_event_info()
    # now we have to map the things to the whats
    recurring_ids = list(set([x["recurring_event_color"] for x in event_info]))

    for item in event_info:
        item["recurring_event_color"] = recurring_ids.index(item["recurring_event_color"])
        item["location_name"] = item["location"]
        # map the locations to the coords
        geolocator = Nominatim()
        print item["location"]
        location = geolocator.geocode(item["location"])
        if not location:
            print item["location_name"], "fucked up geopy..."
            location = geolocator.geocode("1350 Chestnut Street, Philadelphia, PA, United States")
        item["location"] = {    
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    print event_info
    return json.dumps(event_info)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)