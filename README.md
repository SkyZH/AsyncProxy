# AsyncProxy

Simple Async Proxy written in Python

## Run

Run Proxy before installing Python 3.5 in /usr/local/bin

    git clone git@github.com:SkyZH/AsyncProxy.git && cd AsyncProxy
    chmod 777 main_client.py
    chmod 777 main_echoserver.py
    chmod 777 main_server.py

Then run three python programs.

    ./main_echoserver.py

This is the target server that client wants to connect.
It will send `Hello! You're receiving data from Echo Server.` to the client
and then close the connection.

    ./main_server.py

This is the proxy server.

    ./main_client.py

This is the application using the proxy server to connect to the echo server.
