# Place your imports here
import signal
import socket
import argparse
import logging
import sys

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
    sys.exit(0)

# TODO: Put function definitions here


# Start of program execution
# Parse out the command line server address and port number to listen to
# Set up argument parsing
# Initialize the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, dest='proxyServerPort', default=2100, help="Port for the server to listen on")
parser.add_argument('-a', '--address', type=str, dest='proxyServerAddress', default='localhost', help="Address for the server to bind to")
# Logging level option with default set to 'DEBUG'
parser.add_argument('-l', '--log', type=str, dest='loggingLevel', default='DEBUG', help="Logging level")

# Parse the arguments
args = parser.parse_args()

# Configure logging to 'DEBUG' level and output to 'debugging.txt'
logging.basicConfig(filename='debugging.txt', level=logging.DEBUG, filemode='w')
# Set up signal handling (ctrl-c)
signal.signal(signal.SIGINT, ctrl_c_pressed)

# TODO: Set up sockets to receive requests

# IMPORTANT!
# Immediately after you create your proxy's listening socket add
# the following code (where "skt" is the name of the socket here):
# skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Without this code the autograder may cause some tests to fail
# spuriously.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_skt:

    listen_skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_skt.bind((args.proxyServerAddress, args.proxyServerPort))


    listen_skt.listen()

    
    while True:
        skt, client_address = listen_skt.accept()
        client_request_bytes = b''
        # read from the client until a double newline is received
        while b"\r\n\r\n" not in client_request_bytes:
            client_request_bytes += skt.recv(1024)

        # check if the message that just came is valid
        client_request_lines = client_request_bytes.split(b"\r\n")
        logging.debug("Client sent: %s",client_request_lines)
        if len(client_request_lines[0].split(b" ")) != 3:
            logging.debug("Bad Request")
            skt.send(b"HTTP/1.0 501 Not implemented")
            skt.close()
            continue



        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.connect(("localhost", 80))
                logging.debug("Server connected")
    
            except Exception as e:
                logging.error(f"Error connecting to server: {e}")
            
            server_socket.send(client_request_bytes)

            # keep reading to fully receive response from server
            server_response_bytes = b""
            while True:
                just_received = server_socket.recv(1024)
                server_response_bytes += just_received
                if just_received == b'':
                     break

            # forward message from server back to client
            skt.send(server_response_bytes)
            skt.close()
            server_socket.close()