from attr import attrs, attrib
from . import AliceObject


@attrs
class EntityValue(AliceObject):
    """EntityValue object"""

    # YANDEX.FIO
    first_name = attrib(default=None, type=str)
    patronymic_name = attrib(default=None, type=str)
    last_name = attrib(default=None, type=str)

    # YANDEX.GEO
    country = attrib(default=None, type=str)
    city = attrib(default=None, type=str)
    street = attrib(default=None, type=str)
    house_number = attrib(default=None, type=str)
    airport = attrib(default=None, type=str)

    # YANDEX.DATETIME
    year = attrib(default=None, type=str)
    year_is_relative = attrib(default=False, type=bool)
    month = attrib(default=None, type=str)
    month_is_relative = attrib(default=False, type=bool)
    day = attrib(default=None, type=str)
    day_is_relative = attrib(default=False, type=bool)
    hour = attrib(default=None, type=str)
    hour_is_relative = attrib(default=False, type=bool)
    minute = attrib(default=None, type=str)
    minute_is_relative = attrib(default=False, type=bool)
