import asyncio
import config
import struct

class DawnClientProtocol(asyncio.Protocol):
    def __init__(self, loop, dest_addr, dest_port):
        self.loop = loop
        self.dest_addr = dest_addr
        self.dest_port = dest_port
        self.transport = None

    def _get_addr_buffer(self):
        __addr_data = self.dest_addr.encode()
        __port_data = struct.pack("H", self.dest_port)
        return bytes([]).join([
            bytes([len(__port_data)]),
            __port_data,
            bytes([len(__addr_data)]),
            __addr_data
        ]).ljust(config.STAGE["HEADER"]["HEADER_LENGTH"])


    def connection_made(self, transport):
        print("[NOTICE] Connection Established, Sending Header")
        transport.write(self._get_addr_buffer())
        print("[NOTICE] Header Sent")

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()
