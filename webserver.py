from bird import *
from flask import Flask
from utils import *

app = Flask(__name__)

dev = hexrandom(16)
print(dev)

b = BirdClient(deviceId=dev)
b.setLocation(48.8427614,2.3371797)
while True:
    try:
        b.connect(dev)
        break
    except Exception as e:
        print(e)


#@app.route('/')
#def index():
#    return """
#    <html><head><title>Chirping birds everywhere</title></head><body>
#    <p id="demo"></p>
#    <script>
#    var x = document.getElementById("demo");
#    function getLocation(){
#    if (navigator.geolocation) {
#        navigator.geolocation.getCurrentPosition(processPos);
#    }else{
#        x.innerHTML = "Geoloc Error";
#    }
#
#    function processPos(position){
#    x.innerHTML = "Latitude : " + position.coords.latitude + " Longitude : " + position.coords.longitude;
#    }
#    }
#
#    getLocation();
#    </script>
#    </body></html>
#    """

@app.route('/ring/<float:latitude>/<float:longitude>')
@app.route('/ring/<float:latitude>/<float:longitude>/<int:radius>')
def ring(latitude, longitude, radius=0):
    print("{},{}".format(latitude, longitude))
    latitude = "{0:.7f}".format(latitude)
    longitude = "{0:.7f}".format(longitude)
    
    b.radius = radius
    b.setLocation(float(latitude),float(longitude))
    print("Location set")
    ringAllBirds(b, 50, 1)

    return "Done"
