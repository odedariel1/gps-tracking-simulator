from classes.ClientData import ClientData
from classes.Status import Status
from datetime import datetime
from decimal import Decimal
import socket
import sys
import time
import threading


def client_socket_func(client):
    header_length = 10
    ip = "127.0.0.1"
    port = 1234
    my_username = f"{client.id}"
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a given ip and port
        client_socket.connect((ip, port))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes
        # then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{header_length}}".encode('utf-8')
        client_socket.send(username_header + username)
        print(username_header + username)
        while True:

            # Wait for user to input a message
            message = f"{client}"

            # If message is not empty - send it
            if message:

                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = message.encode('utf-8')
                message_header = f"{len(message):<{header_length}}".encode('utf-8')
                client_socket.send(message_header + message)
                print(message)
                client.start_mocking()
            time.sleep(10)

    except Exception as e:
        # Any other exception - something happened, exit
        print(f'Reading error: {e}')
        sys.exit()

    finally:
        client_socket.close

# ---------------------------------------------------------------------------------------------------------------------


client1 = ClientData()
client2 = ClientData()

# Set clients mocks
try:
    client1.header = "$GPRMC"
    client1.device_id = 123456789
    client1.timestamp = datetime.strptime("2024-05-21 14:32:10", '%Y-%m-%d %H:%M:%S')
    client1.latitude = Decimal('37.7749')
    client1.longitude = Decimal('-122.4194')
    client1.status = Status.first

    client2.header = "#TRACK"
    client2.device_id = 987654321
    client2.timestamp = datetime.strptime("2024-05-21 14:32:10", '%Y-%m-%d %H:%M:%S')
    client2.latitude = Decimal('34.0522')
    client2.longitude = Decimal('-118.2437')
    client2.status = Status.second

    t1 = threading.Thread(target=client_socket_func, args=(client1,))
    t2 = threading.Thread(target=client_socket_func, args=(client2,))
    t1.start()
    t2.start()

except ValueError as ex:
    print(ex)



