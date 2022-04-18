import asyncio

from aioalice.dispatcher import Dispatcher
from aioalice.dispatcher.webhook import get_new_configured_app, configure_app

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


__version__ = '1.5.1'
