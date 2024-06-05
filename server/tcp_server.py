import socket
import select
import bll
import map_creator


class TcpServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        # Create a socket object with IPv4 addressing (AF_INET) and TCP protocol (SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow the server to reuse the address to avoid 'address already in use' error
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))
        # Start listening for incoming connections
        self.server_socket.listen()
        # Set the server socket to non-blocking mode
        self.server_socket.setblocking(0)
        # List of sockets to monitor for incoming data
        self.inputs = [self.server_socket]
        # List of sockets to monitor for being ready to write (not used here)
        self.outputs = []
        print(f"Server started on {self.host}:{self.port}")

    def handle_client_data(self, client_socket):
        try:
            # Receive data from the client (up to 1024 bytes)
            data = client_socket.recv(1024)
            if data:
                # If data is received, decode and print it
                print(f"{data.decode('utf-8')}")
                # Save the data to a file using the bll module
                bll.save_data_to_file(f"{data.decode('utf-8')}")
                # Optionally, show the map (commented out here)
                map_creator.show_map()
                return True
            else:
                # No data means the connection is closed
                return False
        except Exception as e:
            # Print any error that occurs during data reception
            print(f"Error receiving data: {e}")
            return False

    def start(self):
        try:
            while self.inputs:
                # Use select to wait for any of the sockets to be ready for reading, writing, or have an error
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

                for s in readable:
                    if s is self.server_socket:
                        # If the server socket is readable, accept a new connection
                        client_socket, client_address = self.server_socket.accept()
                        # Set the client socket to non-blocking mode
                        client_socket.setblocking(0)
                        # Add the client socket to the list of sockets to monitor
                        self.inputs.append(client_socket)
                    else:
                        # Handle data from an existing client socket
                        if not self.handle_client_data(s):
                            # If no data is received, close the connection
                            self.inputs.remove(s)
                            s.close()

                for s in exceptional:
                    # Handle exceptional conditions for any socket
                    print(f"Handling exceptional condition for {s.getpeername()}")
                    self.inputs.remove(s)
                    s.close()
        except KeyboardInterrupt:
            print("Server is shutting down.")
        except Exception as e:
            # Print any unexpected errors
            print(f"Unexpected error: {e}")
        finally:
            # Ensure the server socket and all client sockets are closed
            self.close()

    def close(self):
        print("Closing server socket.")
        self.server_socket.close()
        # Close all client sockets
        for s in self.inputs:
            s.close()
        print("Server shutdown complete.")


def main():
    server = TcpServer()
    server.start()

main()
