from attr import attrs, attrib

from aioalice.types import AliceObject, Interfaces
from aioalice.utils import ensure_cls


@attrs
class Meta(AliceObject):
    """Meta object"""
    locale = attrib(type=str)
    timezone = attrib(type=str)
    client_id = attrib(type=str)
    interfaces = attrib(default=None, converter=ensure_cls(Interfaces))
    flags = attrib(factory=list)
