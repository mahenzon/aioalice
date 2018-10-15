from . import exceptions
from .json import json
from .payload import generate_json_payload
from .safe_kwargs import safe_kwargs


def ensure_cls(klass):
    def converter(val):
        if val is None:
            return
        if isinstance(val, dict):
            return klass(**val)
        if isinstance(val, list):
            return [converter(v) for v in val]
        if not isinstance(val, klass):
            return klass(val)
        return val
    return converter
