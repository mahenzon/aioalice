from aioalice.utils import exceptions
from aioalice.utils.json import json
from aioalice.utils.payload import generate_json_payload
from aioalice.utils.safe_kwargs import safe_kwargs


def ensure_cls(klass):
    from aioalice.types.base import AliceObject
    safe_cls = safe_kwargs(klass) if issubclass(klass, AliceObject) else klass

    def converter(val):
        if val is None:
            return
        if isinstance(val, dict):
            return safe_cls(**val)
        if isinstance(val, list):
            return [converter(v) for v in val]
        if not isinstance(val, klass):
            return klass(val)
        return val
    return converter


__all__ = [
    "exceptions",
    "json",
    "generate_json_payload",
    "safe_kwargs",
    "ensure_cls",
]
