from attr import attrs, attrib
from . import AliceObject


@attrs
class Markup(AliceObject):
    """Markup object"""
    dangerous_context = attrib(type=bool)
