import asyncio
import config

class DawnRemoteClientProtocol(asyncio.Protocol):
    def __init__(self, loop, transport):
        self.loop = loop
        self.transport = None
        self.remote_transport = transport

    def connection_made(self, transport):
        print("[NOTICE] Connection Established")
        self.transport = transport

    def data_received(self, data):
        self.remote_transport.write(data)

    def connection_lost(self, exc):
        print("[NOTICE] Remote Closed Connection")
        self.remote_transport.close()
