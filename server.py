from classes.ClientData import ClientData
from classes.Status import Status
from decimal import Decimal
import datetime
import socket
import select
from collections import defaultdict

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


def calc_routh(client):
    routh = 0
    with open(f"data/{client.device_id}.txt", 'r') as file:
        temp_2 = parse_data(file.readline())
        for line in file:
            temp_client = parse_data(line)
            routh += abs(temp_2.latitude - temp_client.latitude) + abs(temp_2.longitude - temp_client.longitude)
            temp_2 = temp_client
    return routh


def distance_from_start(client):
    with open(f"data/{client.device_id}.txt", 'r') as file:
        temp_2 = parse_data(file.readline())
    return abs(temp_2.latitude - client.latitude) + abs(temp_2.longitude - client.longitude)


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
                      f"total routh:{calc_routh(client_data)} "
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
                  f"distance from start:{distance_from_start(client_data)} ")

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

