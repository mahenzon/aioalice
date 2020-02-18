from attr import attrs, attrib

from . import AliceObject
from ..utils import safe_kwargs


@safe_kwargs
@attrs
class Markup(AliceObject):
    """Markup object"""
    dangerous_context = attrib(type=bool)
