from datetime import datetime,timezone
from decimal import Decimal
from classes import client_a, client_b
import socket  # Import the socket module to create a TCP client
import threading
import time


class TCPClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        # Create a socket object with IPv4 addressing (AF_INET) and TCP protocol (SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, device_id):
        self.client_socket.connect((self.host, self.port))  # Connect to the server
        print(f"Connected to server at {self.host}:{self.port} device_id:{device_id}")

    def send_gps(self, data):
        self.client_socket.send(f"{data}".encode('utf-8'))  # Send the message to the server

    def close(self):
        self.client_socket.close()  # Close the client socket
        print("Client socket closed.")


def main(client_data):
    client = TCPClient()  # Create an instance of the TCPClient class
    try:
        client.connect(client_data.device_id)  # Connect to the server
        for _ in range(0, 10):
            client.send_gps(client_data)
            time.sleep(2)
            client_data.start_mocking()  # Send a test message to the server
    except Exception as e:
        print(f"error:{e}")
    finally:
        client.close()  # Ensure the client socket is closed


try:
    client1 = client_a.ClientA("$GPRMC", 123456789, datetime.strptime(datetime.strftime(datetime.now(timezone.utc),
                                                             "%Y-%m-%dT%H:%M:%S.%f")[:-3], "%Y-%m-%dT%H:%M:%S.%f"),
                               Decimal(41.8823), Decimal(12.4581), 1)
    client2 = client_b.ClientB("#TRACK", 987654321, datetime.strptime(datetime.strftime(datetime.now(),
                                                             "%Y-%m-%dT%H:%M:%S.%f")[:-3], "%Y-%m-%dT%H:%M:%S.%f"),
                               Decimal(31.8010), Decimal(34.7991), 'OK')

    t1 = threading.Thread(target=main, args=(client1,))
    t2 = threading.Thread(target=main, args=(client2,))
    t1.start()
    t2.start()

except ValueError as ex:
    print(ex)
