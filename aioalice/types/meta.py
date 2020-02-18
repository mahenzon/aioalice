from attr import attrs, attrib

from . import AliceObject, Interfaces
from ..utils import ensure_cls


@attrs
class Meta(AliceObject):
    """Meta object"""
    locale = attrib(type=str)
    timezone = attrib(type=str)
    client_id = attrib(type=str)
    interfaces = attrib(default=None, convert=ensure_cls(Interfaces))
    flags = attrib(factory=list)
