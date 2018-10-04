from attr import attrs, attrib
from . import AliceObject


@attrs
class EntityToken(AliceObject):
    """EntityToken object"""
    start = attrib(type=int)
    end = attrib(type=int)
