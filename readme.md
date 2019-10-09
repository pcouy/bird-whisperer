# Bird Whisperer

This is a simple script that repeatedly rings the alarm of up to the 250 bird scooter that are closest to the given location. This work is inspired by [the work of The App Analyst](https://theappanalyst.com/bird.html).

It uses [Mailnesia](http://mailnesia.com) to generate accounts with random email on the fly everytime you start the script.

### Update Oct 10, 2019

Bird seems to have taken actions to prevent this from working. I now get a `412 Precontition failed` whenever I try to make a bird chirp, from two different IP addresses. Please try and tell me if it still works for you. 

## Disclaimer

To the best of my knowledge, there is no rate limiting whatsoever on the Bird API. However, [Bird's terms of service](https://www.bird.co/terms/) state the following :

> You agree that you will not use any robot, spider, scraper or other automated means to access the Services for any purpose without our express written permission. Additionally, you agree that you will not: (i) take any action that imposes, or may impose in our sole discretion an unreasonable or disproportionately large load on our infrastructure; (ii) interfere or attempt to interfere with the proper working of the site or any activities conducted on the Services; or (iii) bypass any measures we may use to prevent or restrict access to the Services.

## How to use

First, run `pip3 install -r requirements.txt`

Then you are good to go.

```
$ python3 bird.py -h
usage: bird.py [-h] [-a ADDRESS] [--autopick-address] [-n RINGS] [-t THREADS]
               [-r RADIUS]

Bird API client library. Calling this file directly causes all birds aroud
given location to chirp

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Search for address on OSM and use fetched GPS
                        coordinates
  --autopick-address    If set, automatically picks the first search result
  -n RINGS, --rings RINGS
                        How many times to loop over the birds
  -t THREADS, --threads THREADS
                        How many threads to use
  -r RADIUS, --radius RADIUS
                        Radius around given position in which to ring birds
```

## Master of birds mode

The `webserver.py` script allows to remotely trigger the alarms from URL parameters.
Run the following command on an internet facing server `FLASK_APP=webserver.py python3 -m flask run --host=0.0.0.0 --port=8000`. You will now be able to query `http[s]://{your.hostname}:8000/ring/{latitude}/{longitude}/{radius}`

The `droid.py` script is meant to be run on an Android phone with QPython3. You must first install edit the `HOST` and `PORT` variables to match the public hostname of your server as well as your chosen port.
Then, install the `requests` module via the pip3 installer in QPython3 and make sure the `SL4A` service is running (from the "three dots" menu in the upper right corner of the app). When this is done, run the script from the "Programs" menu. It will continuously fetch your GPS location and ring the alarm of nearby birds as you move around the city by querying the flask server on every location update.

This was put together in a very short time and you might need to start a bogus trip on Google maps to make your phone update your location using GPS more often. When I do not do this, 80% of my location updates are made using network instead of GPS.

## Credits

https://theappanalyst.com/bird.html
