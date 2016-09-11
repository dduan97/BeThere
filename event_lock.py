import datetime
from threading import Lock
from my_calendar import get_events
from geopy.geocoders import Nominatim

EventLock = Lock()

class EventInfo(object):

    def __init__(self):
        self.event_ids_times = None
        self.event_info = None
        self.past_events = []

    # sets self.event_ids_times
    def retrieve_event_ids_times(self):
        print "EventInfo object retrieving events"
        events = get_events()
        current = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
        # list of (id, name, datetime) for all the events
        event_ids_times = map(lambda x: (x["id"], x["summary"], datetime.datetime.strptime(x["start"]["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S" )), events)
        # sort by datetime
        event_ids_times = sorted(event_ids_times, key=lambda x: x[-1])
        # filter out the ones that have happened already
        event_ids_times = filter(lambda x: x[-1] > current, event_ids_times)
        self.event_ids_times = event_ids_times
        return self.event_ids_times

    # sets self.event_info to id, name, start_time, recurring_event_color,
    # and location
    def retrieve_event_info(self):
        events = get_events()

        geolocator = Nominatim()
        # list of (id, name, datetime) for all the events
        event_ids_times = map(lambda x: {
                "id": x["id"], 
                "name": x["summary"], 
                "start_time": x["start"]["dateTime"][:-6],
                "recurring_event_color": x["recurring_event_color"] if "recurringEventID" in events else None,
                "location": {
                    "latitude": geolocator.geocode(x["location"]).latitude if geolocator.geocode(x["location"]) else 39.9506873333333,
                    "longitude": geolocator.geocode(x["location"]).longitude if geolocator.geocode(x["location"]) else -75.1632256666667
                    }
            }, events)
        self.event_info = event_ids_times
        return self.event_info

    # retrieve the event info and then search by id, returning (lat, long)
    def get_location_by_event_id(self, event_id):
        self.retrieve_event_info()
        # now we search through and look for event id
        for item in self.event_info:
            if item["id"] == event_id:
                # get the lat/long and return it
                return item["location"]
        return None

    def get_name_by_event_id(self, event_id):
        self.retrieve_event_info()
        # now we search through and look for event id
        for item in self.event_ids_times:
            print item[0]
            if item[0] == event_id:
                # get the lat/long and return it
                return item[1]
        # now search through past events
        for item in self.past_events:
            print item[0]
            if item[0] == event_id:
                return item[1]
        return None

    def push_to_past_events(self, event_tuple_i_think):
        self.past_events.append(event_tuple_i_think)

# now we instantiate an object of this class
OneEventToRuleThemAll = EventInfo()