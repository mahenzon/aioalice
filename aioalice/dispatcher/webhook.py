import asyncio
import logging
import functools
from aiohttp import web
from ..utils import json
from ..types import AliceRequest, AliceResponse

DEFAULT_WEB_PATH = '/alicewh/'
ALICE_DISPATCHER_KEY = 'ALICE_DISPATCHER'

RESPONSE_TIMEOUT = 1.3  # Max time to response to API is 1.5s


# TODO: Default error response
DEFAULT_ERROR_RESPONSE = {'ok': False}


def get_response(result):
    """
    Make response object from result.

    :param result: dict or AliceResponse
    :return:
    """
    if result is None:
        logging.critical('TODO! Empty response!!')
        return DEFAULT_ERROR_RESPONSE
    if isinstance(result, AliceResponse):
        return result.to_json()
    return result  # If it's not a dict, it may cause an error.


class WebhookRequestHandler(web.View):
    """
    Simple Wehhook request handler for aiohttp web server.

    You need to register that in app:

    .. code-block:: python3

        app.router.add_route('*', '/your/webhook/path', WebhookRequestHadler, name='webhook_handler')

    But first you need to configure application for getting Dispatcher instance from request handler!
    It must always be with key 'ALICE_DISPATCHER'

    .. code-block:: python3

        dp = Dispatcher()
        app['ALICE_DISPATCHER'] = dp

    """

    def get_dispatcher(self):
        """
        Get Dispatcher instance from environment
        """
        return self.request.app[ALICE_DISPATCHER_KEY]

    async def parse_request(self):
        """
        Read request from stream and deserialize it.
        :return: :class:`aioalice.types.AliceRequest`
        """
        data = await self.request.json()
        return AliceRequest(**data)

    async def process_request(self, request):
        """
        You have to respond in less than 1.5 seconds to webhook.

        So... If you process longer than 1.3 (RESPONSE_TIMEOUT) seconds
        webhook automatically respond with FALLBACK VALUE (#TODO)

        :param request:
        :return:
        """
        dispatcher = self.get_dispatcher()
        loop = dispatcher.loop

        # Analog of `asyncio.wait_for` but without cancelling task
        waiter = loop.create_future()
        timeout_handle = loop.call_later(RESPONSE_TIMEOUT, asyncio.tasks._release_waiter, waiter)
        done_cb = functools.partial(asyncio.tasks._release_waiter, waiter)

        fut = asyncio.ensure_future(dispatcher.parse_request(request), loop=loop)
        fut.add_done_callback(done_cb)

        try:
            try:
                await waiter
            except asyncio.futures.CancelledError:
                fut.remove_done_callback(done_cb)
                fut.cancel()
                raise

            if fut.done():
                return fut.result()
            else:
                fut.remove_done_callback(done_cb)
                fut.add_done_callback(self.log_too_long_request)
        finally:
            timeout_handle.cancel()

    def log_too_long_request(self, task):
        """
        Handle response after 1.3 sec (RESPONSE_TIMEOUT)

        :param task:
        :return:
        """
        # TODO
        raise NotImplementedError

    async def post(self):
        """
        Process POST response

        :return: :class:`aiohttp.web.Response`
        """
        request = await self.parse_request()

        result = await self.process_request(request)
        response = get_response(result)
        return web.json_response(response, dumps=json.dumps)


def configure_app(dispatcher, app: web.Application, path=DEFAULT_WEB_PATH):
    """
    You can prepare web.Application for working with webhook handler.

    :param dispatcher: Dispatcher instance
    :param app: :class:`aiohttp.web.Application`
    :param path: Path to your webhook.
    :return:
    """
    app.router.add_route('*', path, WebhookRequestHandler, name='alice_webhook_handler')
    app[ALICE_DISPATCHER_KEY] = dispatcher


def get_new_configured_app(dispatcher, path=DEFAULT_WEB_PATH):
    """
    Create new :class:`aiohttp.web.Application` and configure it.

    :param dispatcher: Dispatcher instance
    :param path: Path to your webhook.
    :return:
    """
    app = web.Application()
    configure_app(dispatcher, app, path)
    return app
