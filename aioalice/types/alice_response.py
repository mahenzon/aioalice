from attr import attrs, attrib

from aioalice.types import AliceObject, BaseSession, Response
from aioalice.utils import ensure_cls


@attrs
class AliceResponse(AliceObject):
    """AliceResponse is a response to Alice API"""

    response = attrib(converter=ensure_cls(Response))
    session = attrib(converter=ensure_cls(BaseSession))
    session_state = attrib(type=dict)
    user_state_update = attrib(type=dict)
    application_state = attrib(type=dict)
    version = attrib(type=str)
