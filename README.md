# Gps Tracking Simulator: 
## How do I get set up? ###
first Run gps-tracking-simulator.server.server_tcp.py in your python compiler (i used Pycharm) <br>
then Run gps-tracking-simulator.clients.client_tcp.py (so the server will get some messages from client) <br>
then Run gps-tracking-simulator.cli_query.query.py  (and follow instructures of the console) <br>
then open in browser gps-tracking-simulator.server.google_map.html (to see the points on the map) <br>

## Used Technology: ###
Python, socket, googlemaps

## Instructions

* Description: A client-server project that will simulate 2 GPS Tracking devices that will send data to the server Each one of the client will have a different type of protocol  
* This project will help you understand file handling, TCP connection, Multithreading, polymorphism, json serialization.


Features:

* Server requirements 

  Able to receive TCP connection 

  Parse the received message and store it in the file (the file name is the ID of the device )
  you can choose the type of the file for better analysis

  CLI for querying each device by device id :

    -all the points from the last-minute

    -measure the distance between a start point and the point

    -count how many points have the same  Latitude in error of 0.10

  calculate the total route 

  Bonus - show points on OpenStreetMap 

* Clients requirements:

  Unique id 

  Generate GPS mock data based on the format in each client

  Move the GPS  in like a snake  game
 
  sending data based on a timer


Client A: 

Initial position  Latitude: 41.89332 | Longitude: 12.482932

Format:  $GPRMC,123456789,2024-05-21 14:32:10,37.7749,-122.4194,1

$GPRMC: Header indicating a standard GPS NMEA message.

123456789: Device ID.

2024-05-21 14:32:10: Timestamp in UTC.

37.7749: Latitude in decimal degrees.

-122.4194: Longitude in decimal degrees.

1: Status code indicating normal operation.


Client B:

Initial position  Latitude: 34.0189043 | Longitude: -119.0355305

Format: #TRACK,987654321,2024-05-21 14:32:10,34.0522,-118.2437,OK

#TRACK: Header indicating the start of the message.

987654321: Device ID.

2024-05-21 14:32:10: Timestamp.

34.0522: Latitude in decimal degrees.

-118.2437: Longitude in decimal degrees.

OK: Status code indicating normal operation.
