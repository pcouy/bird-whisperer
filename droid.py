import requests
import androidhelper
import sys, select, os, time

HOST="your.public.hostname"
PORT=8000 #Flask listening port
RADIUS=0

droid = androidhelper.Android()

droid.makeToast("fetching GPS")
droid.startLocating(10000)

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        break

    droid.startLocating(10000)
    event = droid.eventWait(5000).result
    droid.stopLocating()
    if event is not None and event['name'] == 'location':
        try:
            print("{},{}".format(event['data']['gps']['latitude'], event['data']['gps']['longitude']))
            url = "http://{}:{}/ring/{}/{}/{}".format(HOST,PORT,event['data']['gps']['latitude'], event['data']['gps']['longitude'],RADIUS)
            r = requests.get(url)
            print(r.text)
        except Exception as e:
            print(event['data'])
            print(e) 
#            time.sleep(5)
    droid.eventClearBuffer()
    event = None


droid.stopLocating()
