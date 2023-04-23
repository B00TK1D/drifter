from gps3 import gps3
import time
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

default_on = 1

lat = 0
lon = 0
alt = 0

while True:
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if (data_stream.TPV['alt'] != "n/a"):
              print('Altitude = ', data_stream.TPV['alt'])
              alt = data_stream.TPV['alt']
            if (data_stream.TPV['lat'] != "n/a"):
              print('Latitude = ', data_stream.TPV['lat'])
              lat = data_stream.TPV['lat']
            if (data_stream.TPV['lon'] != "n/a"):
              print('Longitude = ', data_stream.TPV['lon'])
              lon = data_stream.TPV['lon']
    time.sleep(1)
