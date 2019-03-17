from attr import attrs, attrib

from aioalice.utils import safe_kwargs
from . import AliceObject


@safe_kwargs
@attrs
class Interfaces(AliceObject):
    """Interfaces object"""
    account_linking = attrib(factory=dict)
    payments = attrib(factory=dict)
    screen = attrib(factory=dict)
