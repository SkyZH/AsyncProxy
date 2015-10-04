#!/usr/local/bin/python3.5

import asyncio
from client import DawnClientProtocol
from server import DawnServerClientProtocol


loop = asyncio.get_event_loop()

coro = loop.create_server(lambda: DawnServerClientProtocol(loop),
                              '127.0.0.1', 8888)

loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.close()
