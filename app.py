import gps
import math
import time
import threading
import haversine
from flask import Flask, render_template, redirect, request


app = Flask(__name__)

lat = 0
lon = 0

start_lat = 0
start_lon = 0
start_time = 0

running = 0

aircraftheading = 0
aircraftspeed = 0
windheading = 0
windspeed = 0


def haversine_heading(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    heading = math.atan2(math.sin(lon2-lon1)*math.cos(lat2), math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
    heading = math.degrees(heading)
    heading = (heading + 360) % 360
    return heading

def haversine_distance(lat1, lon1, lat2, lon2):
    return haversine.haversine((lat1, lon1), (lat2, lon2), unit=haversine.Unit.NAUTICAL_MILES)

def calculate_wind():
    global windheading, windspeed, start_lat, start_lon, start_time, lat, lon
    if start_lat and start_lon and start_time and lat and lon:
        delta = time.time() - start_time
        # Convert time delta from seconds to hours
        delta = delta / 3600
        windheading = haversine_heading(start_lat, start_lon, lat, lon)
        windspeed = haversine_distance(start_lat, start_lon, lat, lon) / delta



@app.route('/')
def index():
    global lat, lon, aircraftheading, aircraftspeed, windheading, windspeed, running
    gpslock = 0
    if lat and lon:
        gpslock = 1
    if running:
        calculate_wind()
    return render_template('index.html', gpslock=gpslock,aircraftheading=aircraftheading, aircraftspeed=aircraftspeed, windheading=windheading, windspeed=windspeed, running=running)

@app.route('/update', methods=['GET'])
def update():
    global aircraftheading, aircraftspeed
    aircraftheading = request.args.get('aircraftheading')
    aircraftspeed = request.args.get('aircraftspeed')
    return redirect('/')

@app.route('/start', methods=['GET'])
def start():
    global start_lat, start_lon, start_time, lat, lon, running
    start_lat = lat
    start_lon = lon
    start_time = time.time()
    running = 1
    return redirect('/')

@app.route('/stop', methods=['GET'])
def stop():
    global running
    running = 0
    return redirect('/')


def webserver():
    app.run(host='0.0.0.0', port=80)

def gps_loop():
    global lat, lon
    gpsd = gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
    while True:
        nx = gpsd.next()
        if nx['class'] != 'TPV':
            continue
        lat = getattr(nx,'lat', 0)
        lon = getattr(nx,'lon', 0)
        time.sleep(1)



def main():
    t1 = threading.Thread(target=webserver)
    t2 = threading.Thread(target=gps_loop)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()