from attr import attrs, attrib

from . import AliceObject, BaseSession, Response
from ..utils import ensure_cls


@attrs
class AliceResponse(AliceObject):
    """AliceResponse is a response to Alice API"""

    response = attrib(convert=ensure_cls(Response))
    session = attrib(convert=ensure_cls(BaseSession))
    version = attrib(type=str)
