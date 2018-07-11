from attr import attrs, attrib
from . import AliceObject, Meta, Session, Request, Response, AliceResponse
from aioalice.utils import ensure_cls


@attrs
class AliceRequest(AliceObject):
    """AliceRequest is a request from Alice API"""

    meta = attrib(convert=ensure_cls(Meta))
    request = attrib(convert=ensure_cls(Request))
    session = attrib(convert=ensure_cls(Session))
    version = attrib(type=str)

    def response(self, responose_or_text, **kwargs):
        if not isinstance(responose_or_text, Response):
            responose_or_text = Response(responose_or_text, **kwargs)
        return AliceResponse(
            response=responose_or_text,
            session=self.session.base,
            version=self.version,
        )
