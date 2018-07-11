from attr import attrs, asdict


@attrs
class AliceObject(object):
    """AliceObject is base class for all Alice requests related objects"""

    def to_json(self):
        return asdict(self)
