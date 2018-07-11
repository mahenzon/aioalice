from .json import json
from .payload import generate_json_payload


def ensure_cls(klass):
    def converter(val):
        if isinstance(val, dict):
            return klass(**val)
        if isinstance(val, list):
            return [converter(v) for v in val]
        return val
    return converter
