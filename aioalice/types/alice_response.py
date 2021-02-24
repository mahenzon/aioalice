from attr import attrs, attrib

from aioalice.types import AliceObject, BaseSession, Response
from aioalice.utils import ensure_cls


@attrs
class AliceResponse(AliceObject):
    """AliceResponse is a response to Alice API"""

    response = attrib(converter=ensure_cls(Response))
    session = attrib(converter=ensure_cls(BaseSession))
    version = attrib(type=str)
