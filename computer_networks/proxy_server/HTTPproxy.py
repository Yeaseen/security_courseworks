# Place your imports here
import signal
from socket import *
import argparse
import logging
import sys
import threading
from datetime import datetime

# DS for handling caching
cache_isEnabled = False
cache = {} #(host,server):(server_response,received_time)

# DS for managing blocking 
blocklist = [] #list of blocked hosts with port number
blocklist_isEnabled = False

# Generic responses to the client
HTTP_OK_RESPONSE = b"HTTP/1.0 200 OK"
HTTP_BAD_REQUEST_RESPONSE = b"HTTP/1.0 400 Bad Request"
HTTP_FORDBIDDEN_RESPONSE = b"HTTP/1.0 403 Forbidden"
HTTP_NOT_IMPLEMENTED_RESPONSE = b"HTTP/1.0 501 Not Implemented"

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
    sys.exit(0)

# TODO: Put function definitions here

# Convert Python datetime to HTTP-Date bytestring
def to_http_date(dt : datetime):
    return "{}, {} {} {} {}:{}:{} {}".\
        format(dt.weekday(), dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, dt.tzname()).encode("utf8")

# Sends response msg to client
def respond_to_client(client_skt, msg):
    client_skt.send(msg)
    client_skt.close()

# Send a reqeust to server specified and return response as bytestring
def request_to_server(path, host, headers, server_port):
    # construct the message to send to the server
    request_to_origin_server = b"GET " + path + b" HTTP/1.0\r\n"
    request_to_origin_server += b"Host: " + host + b"\r\n"
    for header in headers:
        request_to_origin_server += header + b': ' + headers[header] + b'\r\n'
    request_to_origin_server += b"\r\n" # don't forget the last newline to end the communication!

    # send the request to the origin server
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        host_as_string = str(host)[2:-1]
        server_socket.connect((host_as_string, server_port))
        server_socket.send(request_to_origin_server)

        # keep reading until the server finishes sending
        server_response_bytes = b""
        while True:
            latest_chunk = server_socket.recv(1024)
            server_response_bytes += latest_chunk
            if latest_chunk == b'':
                break
        #logging.debug("Origin Server response: "+ server_response_bytes)
    return server_response_bytes


# Handle a client connection to HTTPproxy by contacting origin server and sending back response
def handle_connection(skt, client_address):
    client_request_bytes = b''
    # read from the client until a double newline is received
    while b"\r\n\r\n" not in client_request_bytes:
        client_request_bytes += skt.recv(1024)

    # logging.debug("Client Msg: "+ client_request_bytes)
    # check if the message that just came is valid
    # slice the whole request line-by-line
    client_request_lines = client_request_bytes.split(b"\r\n")

    if len(client_request_lines[0].split(b" ")) != 3:
        respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
    for i in range (1, len(client_request_lines)):
        if client_request_lines[i] != b"":
            current_header_line_components = client_request_lines[i].split(b": ")
            for item in current_header_line_components:
                print(item)
            if len(current_header_line_components) != 2:
                respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
                return
            if b" " in current_header_line_components[0]:
                respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
                return

    # extract http components by parsing
    method, url, version = client_request_lines[0].split(b" ", 2)

    # if the method is not valid, respond appropriately and listen for a new socket
    if method == b'HEAD' or method == b'POST':
        respond_to_client(skt, HTTP_NOT_IMPLEMENTED_RESPONSE)
        return
    elif method != b'GET':
        respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
        return
    elif version != b"HTTP/1.0":
        respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
        return
    
    headers = {}
    for i in range (1, len(client_request_lines)):
        if client_request_lines[i] != b"":
            key, value = client_request_lines[i].split(b": ")
            headers[key] = value

    # assign any “Connection” header received from the client with value "close"
    headers[b"Connection"] = b"close"

    # parse the URL
    if b"://" not in url:
        respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
        return
    scheme, url = url.split(b"://", 1)
    if b"/" not in url:
        respond_to_client(skt, HTTP_BAD_REQUEST_RESPONSE)
        return
    host, url = url.split(b"/", 1)
    server_port = 80
    if b":" in host:
            host, server_port = host.split(b":", 1)
            server_port = int(str(server_port)[2:-1])
    path = b'/' + url

    # look for a special path
    # lock the global variables to be used
    global cache, cache_isEnabled, blocklist, blocklist_isEnabled
    if path == b"/proxy/cache/enable":
        cache_isEnabled = True
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path == b"/proxy/cache/disable":
        cache_isEnabled = False
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path == b"/proxy/cache/flush":
        cache.clear()
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path == b"/proxy/blocklist/enable":
        blocklist_isEnabled = True
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path == b"/proxy/blocklist/disable":
        blocklist_isEnabled = False
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path.startswith(b"/proxy/blocklist/add"):
        to_add = path.split(b"/proxy/blocklist/add")[1][1:]
        if b':' in to_add:
            to_add = to_add.split(b':')[0]
        blocklist.append(to_add)
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path.startswith(b"/proxy/blocklist/remove"):
        to_remove = path.split(b"/proxy/blocklist/remove")[1][1:]
        if b':' in to_remove:
            to_remove = to_remove.split(b':')[0]
        blocklist.remove(to_remove)
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    elif path == b"/proxy/blocklist/flush":
        blocklist.clear()
        respond_to_client(skt, HTTP_OK_RESPONSE)
        return
    
    # consult the blocklist
    if blocklist_isEnabled:
        for item in blocklist:
            if item in host:
                respond_to_client(skt, HTTP_FORDBIDDEN_RESPONSE)
                return  

    # look for cache hit
    cache_key = (host, server_port)
    if cache_isEnabled and (cache_key in cache):
        cached_object, time_of_cache = cache[cache_key]
        headers[b"If-Modified-Since"] = to_http_date(time_of_cache)
        server_response_bytes = request_to_server(path, host, headers, server_port)
        
        # check if the content has been modified since it was cached
        if (b'304' in server_response_bytes.split(b'\r\n')[0]):
            server_response_bytes = cached_object
        else:
            cache[cache_key] = (server_response_bytes, datetime.now())
        
        # forward message from server back to client
        respond_to_client(skt, server_response_bytes)
        return  
        
    # consult origin server, cache, and respond to client
    server_response_bytes = request_to_server(path, host, headers, server_port)
    if cache_isEnabled:
        cache[cache_key] = (server_response_bytes, datetime.now())
    respond_to_client(skt, server_response_bytes)


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

    listen_skt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #reusing the same adress
    listen_skt.bind((args.proxyServerAddress, args.proxyServerPort))
    listen_skt.listen()

    # listening for new connection requests from client
    while True:
        proxy_client_skt, client_address = listen_skt.accept()
        #handle_connection(skt,client_address)
        #logging.debug("Client Connected: "+ client_address)
        each_client_thread = threading.Thread(target=handle_connection, args=(proxy_client_skt, client_address))
        each_client_thread.start()