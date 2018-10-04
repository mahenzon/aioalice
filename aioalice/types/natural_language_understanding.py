# Natural Language Understanding: https://medium.com/@lola.com/nlp-vs-nlu-whats-the-difference-d91c06780992
from attr import attrs, attrib
from aioalice.utils import ensure_cls
from . import AliceObject, Entity


@attrs
class NaturalLanguageUnderstanding(AliceObject):
    """Natural Language Understanding object"""
    tokens = attrib(factory=list)
    entities = attrib(factory=list, convert=ensure_cls(Entity))
