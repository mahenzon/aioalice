from attr import attrs, attrib
from . import AliceObject


@attrs
class Meta(AliceObject):
    """Meta object"""
    locale = attrib(type=str)
    timezone = attrib(type=str)
    client_id = attrib(type=str)
