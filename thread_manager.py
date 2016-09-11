# so this makes a call to the gcal api at the start and then goes from there

from threading import Thread
import datetime
import time
from bethere import app
from event_push import send_notif
from my_calendar import get_events
from event_lock import EventLock, OneEventToRuleThemAll

import os

# this gives you only id name and datetime for the events
def get_event_ids_times():
    events = get_events()
    current = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    # list of (id, name, datetime) for all the events
    event_ids_times = map(lambda x: (x["id"], x["summary"], datetime.datetime.strptime(x["start"]["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S" )), events)
    # sort by datetime
    event_ids_times = sorted(event_ids_times, key=lambda x: x[-1])
    # filter out the ones that have happened already
    event_ids_times = filter(lambda x: x[-1] > current, event_ids_times)
    return event_ids_times

class AppThread(Thread):

    def run(self):
        print "running app thread"
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, use_reloader=False)

class PushThread(Thread):

    def run(self):
        EventLock.acquire()
        # a list of tuples (id, name, time)
        event_ids_times = OneEventToRuleThemAll.retrieve_event_ids_times()
        EventLock.release()

        print "starting with {} events".format(len(event_ids_times))
        while True:
            print "running push thread"
            time.sleep(30)
            # get the current time and the time of the first event
            current = datetime.datetime.utcnow() - datetime.timedelta(hours=4) + datetime.timedelta(minutes=1)
            print "getting event"
            print event_ids_times
            if event_ids_times:
                print "checking event with time {}".format(event_ids_times[0][-1])
                print "current time is {}".format(current)
                if current > event_ids_times[0][-1]:
                    # then it's time to push
                    print "time to push", event_ids_times[0][1]
                    event_id = event_ids_times[0][0]

                    EventLock.acquire()
                    OneEventToRuleThemAll.push_to_past_events(event_ids_times[0])
                    EventLock.release()
                    
                    event_ids_times.pop(0)
                    print "event id is ", event_id
                    send_notif(silent=True, event_id=event_id)
            else:
                print "no events left"
                print event_ids_times

            EventLock.acquire()
            print "checking for new events"
            event_ids_times = OneEventToRuleThemAll.retrieve_event_ids_times()
            print "{} events found".format(len(event_ids_times))
            EventLock.release()


# start the two threads
app_thread = AppThread()
push_thread = PushThread()

app_thread.start()
push_thread.start()