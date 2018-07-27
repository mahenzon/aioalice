from attr import attrs, attrib
from . import AliceObject


@attrs
class CardHeader(AliceObject):
    """This object represents a card's header"""
    text = attrib(type=str)
