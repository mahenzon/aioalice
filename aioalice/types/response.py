from attr import attrs, attrib
from aioalice.utils import ensure_cls
from . import AliceObject, Card, Button


@attrs
class Response(AliceObject):
    """Response object"""

    text = attrib(type=str)
    tts = attrib(default=None, type=str)
    card = attrib(default=None, convert=ensure_cls(Card))
    buttons = attrib(default=None, convert=ensure_cls(Button))
    end_session = attrib(default=False, type=bool)
