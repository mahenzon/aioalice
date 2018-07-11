from attr import attrs, attrib
from . import AliceObject


@attrs
class BaseSession(AliceObject):
    """Base Session object"""
    session_id = attrib(type=str)
    message_id = attrib(type=int)
    user_id = attrib(type=str)


@attrs
class Session(BaseSession):
    """Session object"""
    new = attrib(type=bool)
    skill_id = attrib(type=str)

    @property
    def base(self):
        return BaseSession(
            self.session_id,
            self.message_id,
            self.user_id
        )
