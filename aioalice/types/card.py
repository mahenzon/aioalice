from attr import attrs, attrib

from aioalice.utils import ensure_cls
from aioalice.utils.helper import Helper, HelperMode, Item
from . import AliceObject, MediaButton, Image, CardHeader, CardFooter


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
    def big_image(cls, image_id, title, description, button=None):
        """
        Generate Big Image card

        :param image_id: Image's id for BigImage Card
        :param title: Image's title for BigImage Card
        :param description: Image's description for BigImage Card
        :param button: Image's button for BigImage Card
        :return: Card
        """
        return cls(
            CardType.BIG_IMAGE,
            image_id=image_id,
            title=title,
            description=description,
            button=button,
        )

    @classmethod
    def items_list(cls, header, items, footer=None):
        """
        Generate Items List card

        :param header: Card's header
        :param items: Card's items - list of `Image` objects
        :param footer: Card's footer
        :return: Card
        """
        return cls(
            CardType.ITEMS_LIST,
            header=header,
            items=items,
            footer=footer,
        )


class CardType(Helper):
    mode = HelperMode.CamelCase

    BIG_IMAGE = Item()  # BigImage
    ITEMS_LIST = Item()  # ItemsList
