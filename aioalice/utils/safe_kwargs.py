# https://gist.github.com/surik00/a6c2804a2d18a2ab75630bb5d93693c8

import inspect
import functools


def check_spec(func: callable, kwargs: dict):
    spec = inspect.getfullargspec(func)
    if spec.varkw:
        return kwargs

    return {k: v for k, v in kwargs.items() if k in spec.args}


def safe_kwargs(func_or_class):
    @functools.wraps(func_or_class)
    def wrap(*args, **kwargs):
        spec = check_spec(func_or_class, kwargs)
        return func_or_class(*args, **spec)

    return wrap
