from attr import attrs, attrib
from . import AliceObject


@attrs
class Interfaces(AliceObject):
    """Interfaces object"""
    screen = attrib(factory=dict)
