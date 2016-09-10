from flask import Flask, request
from geopy.distance import vincenty
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# post a location for an event when it gets to the time
# request should have fields:
# {
#   latitude: float
#   longitude: float
# }
@app.route("/event/<int:event_id>/location", methods=['POST'])
def check_location(event_id):
    body = json.loads(request.data)
    print body, type(body)
    lat = body["latitude"]
    lon = body["longitude"]
    # something with gcal here
    event_coords = (40.7128, -74.0059)
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

if __name__ == "__main__":
    app.run()