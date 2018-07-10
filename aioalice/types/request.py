from attr import attrs, attrib

from aioalice.utils.helper import Helper, HelperMode, Item
from . import AliceObject, Markup


@attrs
class Request(AliceObject):
    """Request object"""
    command = attrib(type=str)
    original_utterance = attrib(type=str)
    type = attrib(type=str)
    markup = attrib(default=None)
    payload = attrib(default=None)

    @type.validator
    def check(self, attribute, value):
        """
        Type can be 'SimpleUtterance' or 'ButtonPressed'
            "SimpleUtterance" — голосовой ввод;
            "ButtonPressed" — нажатие кнопки.
        """
        if value not in RequestType.all():
            raise ValueError(f'Request type must be "SimpleUtterance" or "ButtonPressed", not "{value}"')

    def __attrs_post_init__(self):
        if self.markup is not None:
            self.markup = Markup(**self.markup)


class RequestType(Helper):
    mode = HelperMode.CamelCase

    SIMPLE_UTTERANCE = Item()  # SimpleUtterance
    BUTTON_PRESSED = Item()  # ButtonPressed
