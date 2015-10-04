# AsyncProxy

Simple Async Proxy written in Python

## Run

Run Proxy after installing Python 3.5 in /usr/local/bin

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

    main_client --- Header {"addr": "127.0.0.1", "port": 8234} ---> main_server
    main_server --- Connect ---> main_echoserver
    main_echoserver --- `Hello! You're receiving data from Echo Server.` ---> main_server
    main_server --- 'Hello! You're receiving data from Echo Server.' ---> main_client

## Stage

| Stage     | Data | Description                             |
| :-------- | :--: | --------------------------------------: |
| INIT      | 0    | Do Nothing                              |
| HEADER    | 1    | Receiving Header                        |
| ESTABLISH | 2    | Establishing Connection to Remote Host  |
| DATA      | 3    | Transferring Data                       |


## Application

In the future, DGlobe will open a proxy server for applications to connect.
Header may contain Kademlia User Hash and virtual target port.

## Improvement

Add Protocol of User Datagram Protocol (UDP)

Add Crypt Services
