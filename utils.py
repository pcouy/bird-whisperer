import threading
import json
from queue import Queue
import requests
import hashlib
import random as rand

scooter_queue = Queue()
def ringAllBirds(birdClient, nThreads, nRepeats):
    print_lock = threading.Lock()
    def process_queue():
        while True:
            current_scooter = scooter_queue.get()
            status, distance = birdClient.ringScooter(current_scooter)
            if status != 0:
                with print_lock:
                    print("{} ringed (status  {}, distance {})".format(current_scooter['id'], status, distance))
            scooter_queue.task_done()

    while len(threading.enumerate()) < nThreads+1:
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()

    for i in range(nRepeats):
        scooters = birdClient.getNearbyScooters()


        for scooter in scooters:
            scooter_queue.put(scooter)

    scooter_queue.join()

    print(threading.enumerate())
    print("==========================")
    print("==============================")
        
def addressToGPS(address, pick_first):
    url = "https://nominatim.openstreetmap.org/search"
    payload = {
            'q': address,
            'format': 'json',
            'addressdetails': 2
            }

    r = requests.get(url, params=payload)
    rData = json.loads(r.text)
    for i, place in enumerate(rData):
        print("{}. {} => {},{}".format(i, place["display_name"], place["lat"], place["lon"]))

    if len(rData) == 1 or pick_first:
        return rData[0]["lat"], rData[0]["lon"]
    else:
        choice = None
        while choice not in [str(i) for i in range(len(rData))]:
            choice = input("Pick a result : ")

        return rData[int(choice)]["lat"], rData[int(choice)]["lon"]

def hexrandom(length):
    reval = ""

    while len(reval) <= length:
        x = str(rand.randint(0,50000))
        reval+= hashlib.sha1(x.encode()).hexdigest()

    return reval[:length]

