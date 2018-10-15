from attr import attrs, attrib

from aioalice.utils import ensure_cls
from . import AliceObject, MediaButton


@attrs
class Image(AliceObject):
    """Image object"""
    image_id = attrib(type=str)
    title = attrib(type=str)
    description = attrib(type=str)
    button = attrib(default=None, convert=ensure_cls(MediaButton))
