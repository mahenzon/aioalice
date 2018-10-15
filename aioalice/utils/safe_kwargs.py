# https://gist.github.com/surik00/a6c2804a2d18a2ab75630bb5d93693c8

import inspect
import functools


def safe_kwargs(func_or_class):
    spec = inspect.getfullargspec(func_or_class)
    all_args = spec.args

    @functools.wraps(func_or_class)
    def wrap(*args, **kwargs):
        accepted_kwargs = {k: v for k, v in kwargs.items() if k in all_args}
        return func_or_class(*args, **accepted_kwargs)

    return wrap
