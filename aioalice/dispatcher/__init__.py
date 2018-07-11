import asyncio
# import logging

from .handler import Handler
from .storage import BaseStorage, DisabledStorage
from .filters import generate_default_filters, ExceptionsFilter

# from ..types.request import RequestType
# log = logging.getLogger(__name__)


class Dispatcher:

    def __init__(self, loop=None, storage=None):
        # TODO: inculde default handler for 'test' commands
        # TODO: create default handler for exceptions handler
        self.loop = loop or asyncio.get_event_loop()
        self.storage = storage or DisabledStorage()
        self.requests_handlers = Handler()
        self.errors_handlers = Handler()

    async def process_request(self, request):
        try:
            return await self.requests_handlers.notify(request)
        except Exception as e:
            result = await self.errors_handlers.notify(self, request, e)
            if result:
                return result
            raise

    def register_request_handler(self, callback, *, commands=None, contains=None, starts_with=None, request_type=None,
                                 func=None, state=None, regexp=None, custom_filters=None, **kwargs):
        """
        Register handler for AliceRequest

        .. code-block:: python3
            # TODO: add example

        :param callback: function to process request
        :param commands: list of commands
        :param contains: list of lines to search in commands `any([line in command for line in contains])`
        :param starts_with: list of lines to check if command starts with any of them
        :param request_type: Type of the request can be 'SimpleUtterance' or 'ButtonPressed'
        :param func: any callable object (for custom checks)
        :param state: For FSM
        :param regexp: REGEXP
        :param custom_filters: list of custom filters
        :param kwargs:
        """
        if custom_filters is None:
            custom_filters = []

        prepared_filers = generate_default_filters(
            self, *custom_filters, commands=commands, contains=contains,
            starts_with=starts_with, request_type=request_type,
            func=func, state=state, regexp=regexp, **kwargs
        )
        self.requests_handlers.register(callback, prepared_filers)

    def request_handler(self, *custom_filters, commands=None, contains=None, starts_with=None,
                        request_type=None, func=None, state=None, regexp=None, **kwargs):
        """
        Decorator AliceRequest handler

        .. code-block:: python3
            # TODO: add example

        :param callback: function to process request
        :param commands: list of commands
        :param contains: list of lines to search in commands `any([line in command for line in contains])`
        :param starts_with: list of lines to check if command starts with any of them
        :param request_type: Type of the request can be 'SimpleUtterance' or 'ButtonPressed'
        :param func: any callable object (for custom checks)
        :param state: For FSM
        :param regexp: REGEXP
        :param custom_filters: list of custom filters
        :param kwargs:
        :return: decorated function
        """
        def decorator(callback):
            self.register_request_handler(
                callback, commands=commands, contains=contains, starts_with=starts_with, request_type=request_type,
                func=func, state=state, regexp=regexp, custom_filters=custom_filters, **kwargs
            )
            return callback

        return decorator

    def register_errors_handler(self, callback, *, exception=None, func=None):
        """
        Register handler for errors

        :param callback:
        :param exception: you can make handler for specific errors type
        :param func: any callable object (for custom checks)
        """
        filters_list = []
        if func is not None:
            filters_list.append(func)
        if exception is not None:
            filters_list.append(ExceptionsFilter(exception))
        self.errors_handlers.register(callback, filters_list)

    def errors_handler(self, exception=None, func=None):
        """
        Decorator for errors handler

        :param func:
        :param exception: you can make handler for specific errors type
        :param run_task: run callback in task (no wait results)
        :return: decorated function
        """

        def decorator(callback):
            self.register_errors_handler(callback, exception=exception, func=func)
            return callback

        return decorator
