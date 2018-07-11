from .filters import check_filters


class SkipHandler(BaseException):
    """Raise this exception if the handler needs to be skipped"""


class Handler:

    def __init__(self):
        self.handlers = []

    def register(self, handler, filters=None, index=None):
        """
        Register callback

        Filters can be awaitable or not.

        :param handler: coroutine
        :param filters: list of filters
        :param index: you can reorder handlers
        """
        if filters and not isinstance(filters, (list, tuple, set)):
            filters = [filters]
        record = (filters, handler)
        if index is None:
            self.handlers.append(record)
        else:
            self.handlers.insert(index, record)

    def unregister(self, handler):
        """
        Remove handler

        :param handler: callback
        :return:
        """
        for handler_with_filters in self.handlers:
            _, registered = handler_with_filters
            if handler is registered:
                self.handlers.remove(handler_with_filters)
                return True
        raise ValueError('This handler is not registered!')

    async def notify(self, *args):
        """
        Notify handlers

        :param args:
        :return: instance of AliceResponse
            You *have* to return something to answer to API
            Consider returning AliceResponse or prepared JSON
        """

        for filters, handler in self.handlers:
            if await check_filters(filters, args):
                try:
                    return await handler(*args)
                except SkipHandler:
                    continue
