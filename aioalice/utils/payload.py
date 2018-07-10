# import datetime

from . import json

DEFAULT_FILTER = ['self', 'cls']


def generate_json_payload(exclude=[], **kwargs):
    """
    Generate payload

    Usage: payload = generate_json_payload(**locals(), exclude=['foo'])

    :param exclude:
    :param kwargs:
    :return: dict
    """
    return {key: _normalize(value) for key, value in kwargs.items() if
            key not in exclude + DEFAULT_FILTER
            and value is not None
            and not key.startswith('_')}


def _normalize(obj):
    """
    Normalize dicts and lists

    :param obj:
    :return: normalized object
    """
    if isinstance(obj, list):
        return [_normalize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items() if v is not None}
    elif hasattr(obj, 'to_json'):
        return obj.to_json()
    return obj


# def _prepare_arg(value):
#     """
#     Stringify dicts/lists and convert datetime/timedelta to unix-time

#     :param value:
#     :return:
#     """
#     if isinstance(value, (list, dict)) or hasattr(value, 'to_json'):
#         return json.dumps(_normalize(value))
#     # elif isinstance(value, datetime.datetime):
#     #     return round(value.timestamp())
#     # elif isinstance(value, datetime.timedelta):
#     #     now = datetime.datetime.now()
#     #     return int((now + value).timestamp())
#     return value
