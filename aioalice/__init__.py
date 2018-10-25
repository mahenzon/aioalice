import asyncio

from .dispatcher import Dispatcher
from .dispatcher.webhook import get_new_configured_app, configure_app

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


__version__ = '1.2.1'
