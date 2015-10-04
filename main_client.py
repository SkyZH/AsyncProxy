#!/usr/local/bin/python3.5

import asyncio
import time


from client import DawnClientProtocol
from server import DawnServerClientProtocol

starttime = time.clock()

loop = asyncio.get_event_loop()

coro = loop.create_connection(lambda: DawnClientProtocol(loop, "127.0.0.1", 8234),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()

endtime = time.clock()
print("Request completed in %.03f seconds"%(endtime - starttime))
