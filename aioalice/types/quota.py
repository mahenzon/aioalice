from attr import attrs, attrib
from . import AliceObject


@attrs
class Quota(AliceObject):
    """Quota object. Values in bytes"""
    total = attrib(type=int)
    used = attrib(type=int)
    available = attrib(init=False, default=0)

    def __attrs_post_init__(self):
        self.available = self.total - self.used
