import asyncio

from .dispatcher import Dispatcher

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


__version__ = '0.1.0'
