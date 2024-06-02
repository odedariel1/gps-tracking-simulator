from classes.ClientData import ClientData
from classes.Status import Status
from decimal import Decimal
import datetime
import socket
import select
from collections import defaultdict
import os
import gmplot
import math

def show_map():
    # Define your latitude and longitude points
    points = []
    folder = "data"
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    points.append({"latitude": Decimal(line.split("latitude: ")[1].split()[0]),
                                   "longitude": Decimal(line.split("longitude: ")[1].split()[0]),
                                   "name": f"{file_name}"})

    # Calculate the center of the map
    avg_lat = sum(point["latitude"] for point in points) / len(points)
    avg_lon = sum(point["longitude"] for point in points) / len(points)

    # Create a gmplot object centered around the average latitude and longitude
    gmap = gmplot.GoogleMapPlotter(avg_lat, avg_lon, 5)

    # Group points by "name"
    points_by_name = defaultdict(list)
    for point in points:
        points_by_name[point["name"]].append(point)

    # Plot the points and routes by "name"
    for name, pts in points_by_name.items():
        latitudes = [point["latitude"] for point in pts]
        longitudes = [point["longitude"] for point in pts]

        # Scatter plot for the points
        gmap.scatter(latitudes, longitudes, color='maroon', size=50, marker=True)

        # Plot the route connecting the points
        gmap.plot(latitudes, longitudes, 'lightblue', edge_width=2.5)

    # Save the map to an HTML file
    gmap.draw(f'google_map.html')


def parse_data(string_data):
    client = ClientData()
    client.header = string_data.split("header: ")[1].split()[0]
    client.device_id = int(string_data.split("device_id: ")[1].split()[0])
    date = string_data.split("timestamp: ")[1].split()
    client.timestamp = datetime.datetime.strptime(date[0] + " " + date[1], '%Y-%m-%d %H:%M:%S')
    client.latitude = Decimal(string_data.split("latitude: ")[1].split()[0])
    client.longitude = Decimal(string_data.split("longitude: ")[1].split()[0])
    status = string_data.split("status: ")[1].split()[0]
    if len(status) == 1:
        client.status = Status(int(string_data.split("status: ")[1].split()[0]))
    else:
        client.status = Status(string_data.split("status: ")[1].split()[0])
    return client


def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(lambda x: round(math.radians(x), 5), [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of Earth in kilometers. Use 3956 for miles.
    r = 6371
    # Calculate the distance
    distance = c * r
    return round(distance, 4)


def calc_routh(client):
    routh = 0
    with open(f"data/{client.device_id}.txt", 'r') as file:
        temp_2 = parse_data(file.readline())
        for line in file:
            temp_client = parse_data(line)
            routh += haversine(temp_client.latitude, temp_client.longitude, temp_2.latitude, temp_2.longitude)
            temp_2 = temp_client
    return routh


def distance_from_start(client):
    with open(f"data/{client.device_id}.txt", 'r') as file:
        temp_2 = parse_data(file.readline())
    return haversine(client.latitude, client.longitude, temp_2.latitude, temp_2.longitude)


def count_same_latitude(client):
    count_dic = defaultdict(int)
    with open(f"data/{client.device_id}.txt", 'r') as file:
        for line in file:
            temp_client = parse_data(line)
            count_dic[f'{temp_client.latitude}'] += 1
    count = 0
    for value in count_dic.values():
        if value > 1:
            count += value
    return count


def receive_mock(client_socket):
    try:
        # Receive a mock from the client
        message_header = client_socket.recv(header_length)
        # If we received no data, client gracefully closed a connection, for example using socket.close()
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


header_length = 10
ip = "127.0.0.1"
port = 1234

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set Reconnection
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the host and a port
server_socket.bind((ip, port))

# Start listening for incoming connections
server_socket.listen()
print("Server is listening...")

# List of sockets for select.select()
sockets_list = [server_socket]
# List of connected clients - socket as a key, user header and name as data
clients = {}


while True:
    # Read list, Write list, Error On list
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # Accept a connection
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established")

            # Client should send his id right away, receive it
            user = receive_mock(client_socket)
            # If False - client disconnected before he sent his id
            if user is False:
                continue
            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            # Also save userid and userid header
            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} "
                  f"id: {user['data'].decode('utf-8')} time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            message = receive_mock(notified_socket)
            if message is False:
                print(f"Closed connection from id: {clients[notified_socket]['data'].decode('utf-8')} "
                      f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                      f"total routh:{calc_routh(client_data)} kilometers "
                      f"error 0.10: {count_same_latitude(client_data)}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            client_data = parse_data(message['data'].decode('utf-8'))
            user = clients[notified_socket]
            print(client_data)
            with open(f"data/{client_data.device_id}.txt", 'a') as file:
                file.write(f"{client_data}"+"\n")
            print(f"received message from id: {user['data'].decode('utf-8')} "
                  f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                  f"distance from start:{distance_from_start(client_data)} kilometers")
            show_map()

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

