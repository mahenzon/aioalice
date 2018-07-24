from attr import attrs, attrib

from . import AliceObject, MediaButton, Image, CardHeader, CardFooter
from aioalice.utils import ensure_cls
from aioalice.utils.helper import Helper, HelperMode, Item


@attrs
class Card(AliceObject):
    """This object represents a Card either of type `BigImage` or `ItemsList`"""

    type = attrib(type=str)

    # for BigImage
    image_id = attrib(default=None, type=str)
    title = attrib(default=None, type=str)
    description = attrib(default=None, type=str)
    button = attrib(default=None, convert=ensure_cls(MediaButton))

    # for ItemsList
    header = attrib(default=None, convert=ensure_cls(CardHeader))
    items = attrib(default=None, convert=ensure_cls(Image))  # List of Image objects

    footer = attrib(default=None, convert=ensure_cls(CardFooter))

    @type.validator
    def check(self, attribute, value):
        """
        Type can be 'BigImage' or 'ItemsList'
            "BigImage" — с одним изображением
            "ItemsList" — с галереей из нескольких изображений
        """
        if value not in CardType.all():
            raise ValueError(f'Card type must be "BigImage" or "ItemsList", not "{value}"')

    @classmethod
    def big_image(cls, image_id, title, description, button, footer):
        return cls(
            CardType.BIG_IMAGE,
            image_id=image_id,
            title=title,
            description=description,
            button=button,
            footer=footer
        )

    @classmethod
    def items_list(cls, header, items, footer):
        return cls(
            CardType.ITEMS_LIST,
            header=header,
            items=items,
            footer=footer
        )


class CardType(Helper):
    mode = HelperMode.CamelCase

    BIG_IMAGE = Item()  # BigImage
    ITEMS_LIST = Item()  # ItemsList
