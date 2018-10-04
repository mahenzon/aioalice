import logging
from attr import attrs, attrib

from aioalice.utils import ensure_cls
from aioalice.utils.helper import Helper, HelperMode, Item
from . import AliceObject, EntityToken, EntityValue

log = logging.getLogger(__name__)


@attrs
class Entity(AliceObject):
    """Entity object"""
    type = attrib(type=str)
    tokens = attrib(convert=ensure_cls(EntityToken))
    value = attrib(convert=ensure_cls(EntityValue))

    @type.validator
    def check(self, attribute, value):
        """Report unknown type"""
        if value not in EntityType.all():
            log.error('Unknown Entity type! `%r`', value)


class EntityType(Helper):
    mode = HelperMode.UPPER_DOT_SEPARATED

    YANDEX_GEO = Item()
    YANDEX_FIO = Item()
    YANDEX_NUMBER = Item()
    YANDEX_DATETIME = Item()
