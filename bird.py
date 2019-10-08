#!/usr/bin/python3

import requests
import json
import time
from mailnesia import Mailnesia
from utils import *
from geopy.distance import distance as geodist

class BirdClient:
    def __init__(self, osVersion = "8.0.0", deviceModel = "Samsung Galaxy S4", deviceName="GalaxyS4", carrierName = "Orange", deviceId = "1234567890abcdef", appVersion = "4.52.0.15", countryCode = 'fr-FR'):
        self.deviceHeaders = {
                'app-version' : appVersion,
                'os-version' : osVersion,
                'user-agent' : "Android - {}".format(osVersion),
                'connection-type' : '4G',
                'device-model' : deviceModel,
                'battery-level' : '80',
                'device-name' : deviceName,
                'carrier-name' : carrierName,
                'device-id' : deviceId,
                'platform' : 'android',
                'bluetooth-state' : 'disabled',
                'app-name' : 'bird',
                'accept-language' : countryCode
                }

        self.domain = "api-bird.prod.birdapp.com"

        self.latitude = None
        self.longitude = None
        self.authorization = None
        self.radius = 0

    def setLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def getLocationHeader(self):
        return json.dumps({
            'accuracy': 12.123456123456123,
            'altitude': None,
            'heading': None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'mocked': False,
            'speed': None
            })

    def connect(self, mailnesiaId):
        email = "{}@mailnesia.com".format(mailnesiaId)
        url = "https://{}/user/login".format(self.domain)
        headers = {'location':self.getLocationHeader(),
                'content-type': 'application/json; charset=UTF-8'}
        headers.update(self.deviceHeaders)

        r = requests.post(url, data=json.dumps({'email':email}), headers = headers)

        rData = json.loads(r.text)
        loginId = rData['id']
        if 'expires_at' in rData:
            mail = Mailnesia(mailnesiaId)
            loginCode = mail.getBirdCode(mail.getMailLinks()[0])

            time.sleep(2)
            url = "https://{}/request/accept".format(self.domain)
            r = requests.put(url, data=json.dumps({'token': loginCode}), headers=headers)
            rData = json.loads(r.text)
        
        if "token" in rData:
            self.authorization = rData["token"]
        else:
            print(r.text)
            raise Exception("Unable to find token")

    def getNearbyScooters(self, radius=5000):
        assert self.authorization is not None

        payload = {
                'latitude': self.latitude,
                'longitude' : self.longitude,
                'radius': "{0:.1f}".format(radius)
                }
        url = "https://{}/bird/nearby".format(self.domain)
        headers = {
                'location': self.getLocationHeader(),
                'authorization': "Bird {}".format(self.authorization)
                }
        headers.update(self.deviceHeaders)

        r = requests.get(url, params=payload, headers=headers)
        rData = json.loads(r.text)

        print("Fetched {} birds".format(len(rData['birds'])))
        print(rData.keys())

        return rData['birds']

    def ringScooter(self, scooter):
        assert self.authorization is not None

        birdDistance = geodist((self.latitude,self.longitude), (scooter["location"]["latitude"], scooter["location"]["longitude"]))
        if self.radius == 0 or self.radius >= birdDistance.m:
            url = "https://{}/bird/chirp".format(self.domain)
            headers = {
                    'location': self.getLocationHeader(),
                    'authorization': "Bird {}".format(self.authorization),
                    'content-type': 'application/json; charset=UTF-8'
                    }
            headers.update(self.deviceHeaders)
            payload = {
                    'alarm': False,
                    'bird_id': scooter['id']
                    }

            r = requests.put(url, headers=headers, data=json.dumps(payload))


            payload['alarm'] = True
            r = requests.put(url, headers=headers, data=json.dumps(payload))
        
            return r.status_code, birdDistance
        else:
            return 0, birdDistance



if __name__ == '__main__':
    import argparse
#    import curses
#
#    stdscr = curses.initscr()
#    curses.noecho()
#    curses.cbreak()
#    stdscr.keypad(True)

    parser = argparse.ArgumentParser(description="Bird API client library. Calling this file directly causes all birds aroud given location to chirp")
    parser.add_argument('-a', '--address', type=str, help="Search for address on OSM and use fetched GPS coordinates", default="")
    parser.add_argument('--autopick-address', action='store_true', help="If set, automatically picks the first search result")
#    parser.add_argument('-c', '--coords', nargs=2, help="Manually select coordinates in the format 'lat long' (unused for now)")
    parser.add_argument('-n', '--rings', type=int, default=10, help="How many times to loop over the birds")
    parser.add_argument('-t', '--threads', type=int, default=50, help="How many threads to use")
    parser.add_argument('-r', '--radius', type=float, default=0, help="Radius around given position in which to ring birds")
    args = parser.parse_args()

    print(args.coords)
    if args.address != "":
        lat, lon = addressToGPS(args.address, args.autopick_address)

    dev = hexrandom(16)
    b = BirdClient(deviceId=dev)
    b.radius = args.radius
    b.setLocation(lat, lon)
    b.connect(dev)

    ringAllBirds(b, args.threads, args.rings)
