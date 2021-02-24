from attr import attrs, attrib

from aioalice.types import AliceObject, MediaButton
from aioalice.utils import ensure_cls


@attrs
class CardFooter(AliceObject):
    """This object represents a card's footer"""
    text = attrib(type=str)
    button = attrib(default=None, converter=ensure_cls(MediaButton))
