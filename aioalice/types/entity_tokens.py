from attr import attrs, attrib
from . import AliceObject


@attrs
class EntityTokens(AliceObject):
    """EntityTokens object"""
    start = attrib(type=int)
    end = attrib(type=int)
