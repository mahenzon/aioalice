from attr import attrs, attrib, asdict


@attrs
class AliceObject:
    """AliceObject is base class for all Alice requests related objects"""

    _raw_kwargs = attrib(factory=dict, init=False)
    """
    here the raw JSON (dict) will be stored
    for using with compatible API
    """

    def to_json(self):
        data = asdict(self, filter=filter_to_json)
        return data


def filter_to_json(attr, value) -> bool:
    return attr.name != '_raw_kwargs'
