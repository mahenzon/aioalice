"""
https://gist.github.com/mahenzon/a6c2804a2d18a2ab75630bb5d93693c8
"""

import functools
from inspect import isclass, getfullargspec


def safe_kwargs(func_or_class):
    from aioalice.types.base import AliceObject

    spec = getfullargspec(func_or_class)
    all_args = spec.args

    save_raw_kwargs = isclass(func_or_class) and issubclass(func_or_class, AliceObject)

    @functools.wraps(func_or_class)
    def wrap(*args, **kwargs):
        accepted_kwargs = {k: v for k, v in kwargs.items() if k in all_args}
        res = func_or_class(*args, **accepted_kwargs)

        if save_raw_kwargs:
            # saving all kwargs for access to unexpected attrs
            res._raw_kwargs.update(kwargs)

        return res

    return wrap
