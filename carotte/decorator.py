# -*- coding: utf-8 -*-


def _task():
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar

task = _task()
