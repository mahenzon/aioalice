import re
import inspect
import logging

from ..utils.helper import Helper, HelperMode, Item


async def check_filter(filter_, args):
    """
    Helper for executing filter

    :param filter_:
    :param args:
    :param kwargs:
    :return:
    """
    if not callable(filter_):
        raise TypeError(f'Filter must be callable and/or awaitable! Error with {filter_}')

    if inspect.isawaitable(filter_) or inspect.iscoroutinefunction(filter_):
        return await filter_(*args)
    else:
        return filter_(*args)


async def check_filters(filters, args):
    """
    Check list of filters

    :param filters:
    :param args:
    :return:
    """
    if filters is not None:
        for f in filters:
            filter_result = await check_filter(f, args)
            if not filter_result:
                return False
    return True


class Filter:
    """
    Base class for filters
    """

    def __call__(self, *args, **kwargs):
        return self.check(*args, **kwargs)

    def check(self, *args, **kwargs):
        raise NotImplementedError


class AsyncFilter(Filter):
    """
    Base class for asynchronous filters
    """

    def __aiter__(self):
        return None

    def __await__(self):
        return self.check

    async def check(self, *args, **kwargs):
        raise NotImplementedError


class StringCompareFilter(AsyncFilter):
    """
    Base for string comparison
    """

    def __init__(self, lines):
        self.lines = [w.lower() for w in lines]


class StartsWithFilter(StringCompareFilter):
    """
    Check if command starts with one of these lines
    """

    async def check(self, areq):
        command = areq.request.command.lower()
        return any([command.startswith(line) for line in self.lines])


class ContainsFilter(StringCompareFilter):
    """
    Check if command contains one of these lines
    """

    async def check(self, areq):
        command = areq.request.command.lower()
        return any([line in command for line in self.lines])


class CommandsFilter(AsyncFilter):
    """
    Check if command is one of these phrases
    Pass commands in lower case
    """

    def __init__(self, commands):
        self.commands = commands

    async def check(self, areq):
        command = areq.request.command.lower()
        return command in self.commands


class RegexpFilter(Filter):
    """
    Regexp filter for original_utterance (full request text)
    If `AliceRequest.request.original_utterance` matches regular expression
    """

    def __init__(self, regexp):
        self.regexp = re.compile(regexp, flags=re.IGNORECASE | re.MULTILINE)

    def check(self, areq):
        return bool(self.regexp.search(areq.request.original_utterance))


class RequestTypeFilter(Filter):
    """
    Check AliceRequest.request type
    On API 1.0 it can be 'SimpleUtterance' or 'ButtonPressed'
    """

    def __init__(self, content_types):
        if isinstance(content_types, str):
            content_types = [content_types]
        self.content_types = content_types

    def check(self, areq):
        return areq.request.type in self.content_types


class ExceptionsFilter(Filter):
    """
    Filter for exceptions
    """

    def __init__(self, exception):
        self.exception = exception

    def check(self, dispatcher, update, exception):
        return isinstance(exception, self.exception)


def generate_default_filters(dispatcher, *args, **kwargs):
    """
    Prepare filters

    :param dispatcher:
    :param args:
    :param kwargs:
    :return:
    """
    filters_list = []

    for name, filter_data in kwargs.items():
        # if filter_data is None and name != DefaultFilters.STATE:
        #     continue
        # TODO: states
        if name == DefaultFilters.REQUEST_TYPE:
            filters_list.append(RequestTypeFilter(filter_data))
        elif name == DefaultFilters.COMMANDS:
            if isinstance(filter_data, str):
                filters_list.append(CommandsFilter([filter_data]))
            else:
                filters_list.append(CommandsFilter(filter_data))
        elif name == DefaultFilters.STARTS_WITH:
            if isinstance(filter_data, str):
                filters_list.append(StartsWithFilter([filter_data]))
            else:
                filters_list.append(StartsWithFilter(filter_data))
        elif name == DefaultFilters.CONTAINS:
            if isinstance(filter_data, str):
                filters_list.append(ContainsFilter([filter_data]))
            else:
                filters_list.append(ContainsFilter(filter_data))
        elif name == DefaultFilters.FUNC:
            filters_list.append(filter_data)
        elif name == DefaultFilters.REGEXP:
            filters_list.append(RegexpFilter(filter_data))
        elif isinstance(filter_data, Filter):
            filters_list.append(filter_data)
        else:
            logging.warning('Unexpected filter with name '
                            f'{name!r} of type `{type(filter_data)}` ({filter_data})')

    filters_list += list(args)  # Some custom filters

    return filters_list


class DefaultFilters(Helper):
    mode = HelperMode.snake_case

    REQUEST_TYPE = Item()  # request_type
    STARTS_WITH = Item()  # starts_with
    CONTAINS = Item()  # contains
    COMMANDS = Item()  # commands
    REGEXP = Item()  # regexp
    FUNC = Item()  # func
