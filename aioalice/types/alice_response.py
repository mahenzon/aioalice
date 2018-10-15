from attr import attrs, attrib
from aioalice.utils import ensure_cls
from . import AliceObject, BaseSession, Response


@attrs
class AliceResponse(AliceObject):
    """AliceResponse is a response to Alice API"""

    response = attrib(convert=ensure_cls(Response))
    session = attrib(convert=ensure_cls(BaseSession))
    version = attrib(type=str)
