from attr import attrs, attrib

from aioalice.utils import safe_kwargs, ensure_cls
from . import AliceObject, Interfaces


@safe_kwargs
@attrs
class Meta(AliceObject):
    """Meta object"""
    locale = attrib(type=str)
    timezone = attrib(type=str)
    client_id = attrib(type=str)
    interfaces = attrib(default=None, convert=ensure_cls(Interfaces))
    flags = attrib(factory=list)
