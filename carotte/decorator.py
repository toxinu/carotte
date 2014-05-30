# -*- coding: utf-8 -*-
from functools import wraps
from functools import partial


def task(method=None, name=None, app=None):
    if method is None:
        return partial(task, app=app, name=name)
    if not name:
        name = method.__name__

    method.delay = lambda *args, **kwargs: app.run_task(name, *args, **kwargs)
    app.registrar[name] = method

    @wraps(method)
    def f(*args, **kwargs):
        registered_task = method(*args, **kwargs)
        return task(registered_task)
    return f
