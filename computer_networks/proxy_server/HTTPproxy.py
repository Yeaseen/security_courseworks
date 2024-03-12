# Place your imports here
import signal
from socket import *
import argparse
import logging
import sys
import threading

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
    sys.exit(0)

# TODO: Put function definitions here

def handle_connection(skt, client_address):
    client_request_bytes = b''
    # read from the client until a double newline is received
    while b"\r\n\r\n" not in client_request_bytes:
        client_request_bytes += skt.recv(1024)
    
    # check if the message that just came is valid
    client_request_lines = client_request_bytes.split(b"\r\n")
    if len(client_request_lines[0].split(b" ")) != 3:
        skt.send(b"HTTP/1.0 400 Bad Request")
        skt.close()
        return
    bad_parse = False
    for i in range (1, len(client_request_lines)):
        if client_request_lines[i] != b"":
            current_header_line_components = client_request_lines[i].split(b": ")
            for item in current_header_line_components:
                print(item)
            if len(current_header_line_components) != 2:
                skt.send(b"HTTP/1.0 400 Bad Request")
                skt.close()
                bad_parse = True
                break
            if b" " in current_header_line_components[0]:
                skt.send(b"HTTP/1.0 400 Bad Request")
                skt.close()
                bad_parse = True
                break
            if bad_parse:
                break
    if bad_parse:
        return
        

    # parse the message
    method, url, version = client_request_lines[0].split(b" ", 2)
    if version != b"HTTP/1.0":
        skt.send(b"HTTP/1.0 400 Bad Request")
        skt.close()
        return
    headers = {}
    for i in range (1, len(client_request_lines)):
        if client_request_lines[i] != b"":
            key, value = client_request_lines[i].split(b": ")
            headers[key] = value

    # if the method is not valid, respond appropriately and listen for a new socket
    if method == b'HEAD' or method == b'POST':
        skt.send(b"HTTP/1.0 501 Not Implemented")
        skt.close()
        return
    elif method != b'GET':
        skt.send(b"HTTP/1.0 400 Bad Request")
        skt.close()
        return

    # assign any “Connection” header received from the client with value "close"
    headers[b"Connection"] = b"close"

    # parse the URL
    if b"://" not in url:
        skt.send(b"HTTP/1.0 400 Bad Request")
        skt.close()
        return
    scheme, url = url.split(b"://", 1)
    if b"/" not in url:
        skt.send(b"HTTP/1.0 400 Bad Request")
        skt.close()
        return
    host, url = url.split(b"/", 1)
    server_port = 80
    if b":" in host:
            host, server_port = host.split(b":", 1)
            server_port = int(str(server_port)[2:-1])
    host_as_string = str(host)[2:-1]
    path = b'/' + url

    # construct the message to send to the server
    to_send = b"GET " + path + b" HTTP/1.0\r\n"
    to_send += b"Host: " + host + b"\r\n"
    for header in headers:
        to_send += header + b': ' + headers[header] + b'\r\n'
    to_send += b"\r\n" # don't forget the last newline to end the communication!

    # send the message to the server
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.connect((host_as_string, server_port))
        server_socket.send(to_send)

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


   #CLient <----> HTTP Proxy  <---> Server

 
with socket(AF_INET, SOCK_STREAM) as listen_skt:

    listen_skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    listen_skt.bind((args.proxyServerAddress, args.proxyServerPort))


    listen_skt.listen()

    
    # wait for connections
    while True:
        skt, client_address = listen_skt.accept()
        #handle_connection(skt,client_address)
        #logging.debug("Client Connected: "+ client_address)
        new_thread = threading.Thread(target=handle_connection, args=(skt, client_address))
        new_thread.start()