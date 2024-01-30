# Client <--> ProxyServer --> Server

## Step 1: Run a Simple PythonServer on loaclhost:80
Created a simple.html file to serve upon ProxyServer's request

```bash
python3 -m http.server 80
```

##Step 2: Run the ProxyServer
Default proxyServerAddress: localhost
Deafult proxyServerPort: 2100

```bash
python3 HTTPproxy.py -a localhost -p 1230 -l DEBUG
```

## Step 3: Client can send the GET request to ProxyServer
The ProxyServer will process this.
If processing failed, ProxyServer will send 501 or 400 to the client
If processined passed, Proxyserver send the request to the Server, receive the server response
and, finally deliver the content to the client.

```bash
echo "GET /simple.html HTTP/1.0\r\n\r\n" | nc localhost 1230
```
