# -*- coding: utf-8 -*-
from .decorator import task
from .worker import Worker
from .client import Client


class Carotte(object):
    def __init__(self, broker=None):
        self.broker = broker
        self.registrar = {}
        self._client = None

    @property
    def client(self):
        if self._client is None:
            opts = {}
            if self.broker:
                opts.update({'broker': self.broker})
            self._client = Client(**opts)
        return self._client

    def configure_client(self, **kwargs):
        self._client = Client(**kwargs)

    def run_task(self, *args, **kwargs):
        return self.client.run_task(*args, **kwargs)

    def task(self, *args, **kwargs):
        if args and not hasattr(args[0], '__call__'):
            raise Exception(
                'All task arguments must be keyword arguments. '
                'Got: "%s"' % args)
        return task(app=self, *args, **kwargs)

    def run_worker(self, **kwargs):
        if not 'bind' in kwargs and self.broker:
            kwargs['bind'] = self.broker
        self.worker = Worker(**kwargs)
        for name, task in self.registrar.items():
            self.worker.add_task(name, task)
        self.worker.run()
