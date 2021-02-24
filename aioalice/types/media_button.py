from attr import attrs, attrib

from aioalice.types import AliceObject


@attrs
class MediaButton(AliceObject):
    """MediaButton object"""
    text = attrib(type=str)
    url = attrib(type=str)
    payload = attrib(default=None)
