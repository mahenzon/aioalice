from attr import attrs, attrib

from aioalice.types import AliceObject, MediaButton
from aioalice.utils import ensure_cls


@attrs
class Image(AliceObject):
    """Image object"""
    image_id = attrib(type=str)
    title = attrib(type=str)
    description = attrib(type=str)
    button = attrib(default=None, converter=ensure_cls(MediaButton))
