#!/usr/local/bin/python3.5

import asyncio
from client import DawnClientProtocol
from server import DawnServerClientProtocol
from socks5server import Socks5Protocol


loop = asyncio.get_event_loop()

coro = loop.create_server(lambda: Socks5Protocol(loop),
                              '127.0.0.1', 1080)

loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.close()
