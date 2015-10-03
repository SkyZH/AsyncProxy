import asyncio
import config

class DawnClientProtocol(asyncio.Protocol):
    def __init__(self, loop, dest_addr):
        self.loop = loop
        self.dest_addr = dest_addr
        self.transport = None

    def _get_addr_buffer(self):
        _encode = self.dest_addr.encode()
        return bytes([]).join([
            bytes([len(_encode)]),
            _encode
        ]).ljust(config.STAGE["HEADER"]["HEADER_LENGTH"])

    def connection_made(self, transport):
        print("[NOTICE] Connection Established, Sending Header")
        transport.write(self._get_addr_buffer())
        print("[NOTICE] Header Sent")

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()
