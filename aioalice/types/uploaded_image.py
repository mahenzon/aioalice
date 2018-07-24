from attr import attrs, attrib
from . import AliceObject


@attrs
class UploadedImage(AliceObject):
    """This object represents an uploaded image"""
    id = attrib(type=str)
    origUrl = attrib(type=str)

    @property
    def orig_url(self):
        return self.origUrl
