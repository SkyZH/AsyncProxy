import asyncio
import config
from remoteclient import DawnRemoteClientProtocol
import common

SOCKS5_SERVER_STAGE_INIT = 0
SOCKS5_SERVER_STAGE_ADDR = 1
SOCKS5_SERVER_STAGE_ESTABLISHING = 2
SOCKS5_SERVER_STAGE_DATA = 3


class Socks5Protocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

        self.buffer = bytes([])

        self.stage = SOCKS5_SERVER_STAGE_INIT

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
            self.remote_transport.write(self.buffer)
            self.buffer = bytes([])
            self.stage = SOCKS5_SERVER_STAGE_DATA
            print("[NOTICE] Stage Changed to DATA")
        except ConnectionRefusedError:
            print("[NOTICE] Failed to Establish Connection")
            self.transport.close()
        except OSError:
            print("[NOTICE] Failed to Establish Connection")
            self.transport.close()

    def data_received(self, data):
        if self.stage == SOCKS5_SERVER_STAGE_DATA:
            self.remote_transport.write(data)
            return

        self.buffer += data

        if self.stage == SOCKS5_SERVER_STAGE_INIT:
            if len(self.buffer) >= config.SOCKS5_STAGE["INIT"]["LENGTH"]:
                self.transport.write(b"\x05\x00")
                self.stage = SOCKS5_SERVER_STAGE_ADDR
                self.buffer = self.buffer[3:]
                print("[NOTICE] Stage Changed to ADDR")
        if self.stage == SOCKS5_SERVER_STAGE_ADDR:
            if len(self.buffer) >= config.SOCKS5_STAGE["ADDR"]["LENGTH"]:
                addrtype, self.remote_addr, self.remote_port, header_length = common.parse_header(self.buffer[3:])
                self.transport.write(b'\x05\x00\x00\x01'
                                     b'\x00\x00\x00\x00\x10\x10')
                self.stage = SOCKS5_SERVER_STAGE_ESTABLISHING
                self.buffer = self.buffer[header_length + 3:]
                print("[NOTICE] Establishing Connection to %s:%d" % (self.remote_addr, self.remote_port))
                asyncio.async(self.connect_remote())
        if self.stage == SOCKS5_SERVER_STAGE_ESTABLISHING:
            pass

    def connection_lost(self, exc):
        if self.remote_transport:
            self.remote_transport.close()
        self.transport.close()
        print("[NOTICE] Local Closed Connection")
