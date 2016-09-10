from flask import Flask, request
from geopy.distance import vincenty
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
    lat = request.data.latitude
    lon = request.data.longitude
    # something with gcal here
    event_coords = (40.7128, -74.0059)
    current_coords = (float(lat), float(lon))

    if vincenty(event_coords, current_coords).feet < 100:
        return "wow you actually made it"
    return "wow youre late wow"


if __name__ == "__main__":
    app.run()