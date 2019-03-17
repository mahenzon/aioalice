from attr import attrs, attrib
from . import AliceObject


@attrs
class Interfaces(AliceObject):
    """Interfaces object"""
    account_linking = attrib(factory=dict)
    payments = attrib(factory=dict)
    screen = attrib(factory=dict)
