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
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items() if v is not None}
    # elif hasattr(obj, 'to_json'):
    #     return _normalize(obj.to_json())
    elif isinstance(obj, list):
        return [_normalize(item) for item in obj]
    return obj
