from attr import attrs, attrib

from aioalice.utils import safe_kwargs, ensure_cls
from aioalice.utils.helper import Helper, HelperMode, Item
from . import AliceObject, Markup, NaturalLanguageUnderstanding


@safe_kwargs
@attrs
class Request(AliceObject):
    """Request object"""
    type = attrib(type=str)
    command = attrib(default='', type=str)  # Can be none if payload passed
    original_utterance = attrib(default='', type=str)  # Can be none if payload passed
    markup = attrib(default=None)
    payload = attrib(default=None)
    nlu = attrib(default=None, convert=ensure_cls(NaturalLanguageUnderstanding))

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
