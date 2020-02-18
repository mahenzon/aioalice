from attr import attrs, attrib

from . import AliceObject, Card, Button
from ..utils import ensure_cls


@attrs
class Response(AliceObject):
    """Response object"""

    text = attrib(type=str)
    tts = attrib(default=None, type=str)
    card = attrib(default=None, convert=ensure_cls(Card))
    buttons = attrib(default=None, convert=ensure_cls(Button))
    end_session = attrib(default=False, type=bool)
