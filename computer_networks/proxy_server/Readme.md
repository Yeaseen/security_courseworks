# Client <--> ProxyServer --> Server

## Step 1: Run a Simple Python Server on localhost:80

Created a `simple.html` file to serve upon ProxyServer's request.

```bash
python3 -m http.server 80
```

## Step 2: Run the ProxyServer

- Default proxyServerAddress: `localhost`
- Default proxyServerPort: `2100`

```bash
python3 HTTPproxy.py -a localhost -p 1230 -l DEBUG
```

## Step 3: Client can send the GET request to ProxyServer

The ProxyServer will process this. If processing fails, ProxyServer will send 501 or 400 to the client. If processing passes, ProxyServer sends the request to the Server, receives the server response, and finally delivers the content to the client.

```bash
echo "GET /simple.html HTTP/1.0\r\n\r\n" | nc localhost 1230

echo "GET http://www.flux.utah.edu/simple.html HTTP/1.0\r\n\r\n" | nc localhost 1230

```