from attr import attrs, attrib
# from attr.validators import instance_of as an
from . import AliceObject, BaseSession, Response
from aioalice.utils import ensure_cls


@attrs
class AliceResponse(AliceObject):
    """AliceResponse is a response to Alice API"""

    # session = attrib(validator=an(BaseSession))
    response = attrib(convert=ensure_cls(Response))
    session = attrib(convert=ensure_cls(BaseSession))
    version = attrib(type=str)
    # buttons = attrib(factory=list)
    # tts = attrib(default=None, type=str)
    # end_session = attrib(default=False, type=bool)
