import asyncio
import config
from remoteclient import DawnRemoteClientProtocol

DAWN_SERVER_STAGE_INIT = 0
DAWN_SERVER_STAGE_HEADER = 1
DAWN_SERVER_STAGE_ESTABLISH = 2
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

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print("[NOTICE] Connection from {}".format(peername))
        self.transport = transport

    def onEstablished(self, future):
        self.remote_protocol, self.transport = future.result()
        self.stage = DAWN_SERVER_STAGE_DATA
        print("[NOTICE] Stage Changed to DATA")

    def data_received(self, data):
        self.buffer += data
        if self.stage == DAWN_SERVER_STAGE_INIT:
            self.stage = DAWN_SERVER_STAGE_HEADER
            print("[NOTICE] Stage Changed to HEADER")
        if self.stage == DAWN_SERVER_STAGE_HEADER:
            if len(self.buffer) < config.STAGE["HEADER"]["HEADER_LENGTH"]:
                pass
            else:
                self.remote_addr = self.buffer[1:self.buffer[0] + 1]
                self.buffer = self.buffer[config.STAGE["HEADER"]["HEADER_LENGTH"]:]
                self.stage = DAWN_SERVER_STAGE_ESTABLISH
                print("[NOTICE] Stage Changed to ESTABLISH")
        if self.stage == DAWN_SERVER_STAGE_ESTABLISH:
            future = asyncio.Future()
            coro = (self.loop).create_connection(
                lambda: DawnRemoteClientProtocol(self.loop, self.transport),
                self.remote_addr,
                8234
            )
            future = asyncio.Future()
            asyncio.async(coro)
            future.add_done_callback(self.onEstablished)
        if self.stage == DAWN_SERVER_STAGE_DATA:
            print(self.buffer())
            self.buffer = bytes([])
