import asyncio
import config
import struct
from remoteclient import DawnRemoteClientProtocol

DAWN_SERVER_STAGE_INIT = 0
DAWN_SERVER_STAGE_HEADER = 1
DAWN_SERVER_STAGE_ESTABLISHING = 2
DAWN_SERVER_STAGE_DATA = 3


class DawnServerClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

        self.buffer = bytes([])

        self.stage = DAWN_SERVER_STAGE_INIT

        self.remote_protocol = None
        self.remote_transport = None

        self.remote_addr = None
        self.remote_port = None

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print("[NOTICE] Connection from {}".format(peername))

    async def connect_remote(self):
        try:
            (self.remote_transport, self.remote_protocol) = await (self.loop).create_connection(
                lambda: DawnRemoteClientProtocol(self.loop, self.transport),
                self.remote_addr,
                self.remote_port
            )
            self.stage = DAWN_SERVER_STAGE_DATA

            print("[NOTICE] Stage Changed to DATA")

            self.remote_transport.write(self.buffer)
            self.buffer = bytes([])
        except ConnectionRefusedError:
            print("[NOTICE] Failed to Establish Connection")
            self.transport.close()

    def data_received(self, data):
        if self.stage == DAWN_SERVER_STAGE_DATA:
            self.remote_transport.write(data)
            return

        self.buffer += data

        if self.stage == DAWN_SERVER_STAGE_INIT:
            self.stage = DAWN_SERVER_STAGE_HEADER
            print("[NOTICE] Stage Changed to HEADER")
        if self.stage == DAWN_SERVER_STAGE_HEADER:
            if len(self.buffer) < config.STAGE["HEADER"]["HEADER_LENGTH"]:
                pass
            else:
                (self.remote_port, ) = struct.unpack("H", self.buffer[1:self.buffer[0] + 1])
                self.remote_addr = self.buffer[self.buffer[0] + 2: self.buffer[self.buffer[0] + 1] + self.buffer[0] + 2].decode()
                self.buffer = self.buffer[config.STAGE["HEADER"]["HEADER_LENGTH"]:]

                self.stage = DAWN_SERVER_STAGE_ESTABLISHING
                print("[NOTICE] Stage Changed to ESTABLISH")
                print("[NOTICE] Establishing Connection to %s:%d" % (self.remote_addr, self.remote_port))
                asyncio.async(self.connect_remote())
        if self.stage == DAWN_SERVER_STAGE_ESTABLISHING:
            pass

    def connection_lost(self, exc):
        self.remote_transport.close()
        self.transport.close()

        print("[NOTICE] Local closed Connection")
