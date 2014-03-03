# -*- coding: utf-8 -*-
from functools import wraps
from functools import partial

from carotte import registrar


def task(method=None, name=None):
    if method is None:
        return partial(task, name=name)

    if name:
        registrar[name] = method
    else:
        registrar[method.__name__] = method

    @wraps(method)
    def f(*args, **kwargs):
        registered_task = method(*args, **kwargs)
        return task(registered_task)
    return f
