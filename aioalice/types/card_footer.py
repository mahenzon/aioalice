from attr import attrs, attrib

from . import AliceObject, MediaButton
from ..utils import ensure_cls


@attrs
class CardFooter(AliceObject):
    """This object represents a card's footer"""
    text = attrib(type=str)
    button = attrib(default=None, convert=ensure_cls(MediaButton))
