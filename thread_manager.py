# so this makes a call to the gcal api at the start and then goes from there

from threading import Thread
import datetime
import time
from bethere import app
from event_push import send_notif
from my_calendar import get_events

def get_event_ids_times():
    events = get_events()
    current = datetime.datetime.now()
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
        app.run()


class PushThread(Thread):

    def run(self):
        past_events = []
        events = get_events()
        past_events = []
        event_ids_times = get_event_ids_times()

        print "starting with {} events".format(len(event_ids_times))
        while True:
            print "running push thread"
            time.sleep(30)
            # get the current time and the time of the first event
            current = datetime.datetime.now()
            print "getting event"
            print event_ids_times
            if event_ids_times:
                print "checking event"
                if current > event_ids_times[0][-1]:
                    # then it's time to push
                    print "time to push", event_ids_times[0][1]
                    past_events.append(event_ids_times[0])
                    event_ids_times.pop(0)
                    send_notif("test event time up thing...fuck yeah!")
                    # events = get_events()
                    # print "pulled {} events".format(len(events))
                    # # list of (id, datetime) for all the events
                    # event_ids_times = map(lambda x: (x["id"], x["summary"], datetime.datetime.strptime(x["start"]["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S" )), events)
                    # # now we sort it by the datetime
                    # event_ids_times = sorted(event_ids_times, key=lambda x: x[-1])
                    # print event_ids_times
            else:
                print "no events left"
                # now we get the new events
                event_ids_times = get_event_ids_times()
                print event_ids_times


# start the two threads
app_thread = AppThread()
push_thread = PushThread()

app_thread.start()
push_thread.start()