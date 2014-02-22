#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
import base64


class Task(object):
    def __init__(self, id, name, args=[], kwargs={}, client=None):
        self.id = id
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.__terminated = False
        self.__result = None
        self.__success = None
        self.__exception = None

        self.client = client

    def serialize(self):
        data = {
            'id': self.id,
            'name': self.name,
            'args': base64.b64encode(pickle.dumps(self.args)).decode('utf-8'),
            'kwargs': base64.b64encode(pickle.dumps(self.kwargs)).decode('utf-8'),
            'result': self.__result,
            'terminated': self.__terminated,
            'success': self.__success,
            'exception': self.__exception}
        return json.dumps(data)

    def deserialize(self, data):
        data = json.loads(data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.set_terminated(data.get('terminated'))
        self.set_result(data.get('result'))
        self.set_success(data.get('success'))
        self.set_exception(data.get('exception'))

        self.args = []
        if data.get('args'):
            self.args = pickle.loads(base64.b64decode(data.get('args')))
        self.kwargs = {}
        if data.get('kwargs'):
            self.kwargs = pickle.loads(base64.b64decode(data.get('kwargs')))

    @property
    def result(self):
        if self.__terminated:
            return self.__result
        self.__update_task()
        return self.__result

    @property
    def success(self):
        if self.__terminated:
            return self.__success
        self.__update_task()
        return self.__success

    @property
    def exception(self):
        if self.__terminated:
            return self.__exception
        self.__update_task()
        return self.__exception

    @property
    def terminated(self):
        if self.__terminated:
            return self.__terminated
        self.__update_task()
        return self.__terminated

    def set_result(self, result):
        self.__result = result

    def set_success(self, success):
        self.__success = success

    def set_exception(self, exception):
        self.__exception = exception

    def set_terminated(self, terminated):
        self.__terminated = terminated

    def __update_task(self):
        if self.client is None:
            return
        task = self.client.get_task_result(self.id)
        self.__result = task.get('result')
        self.__success = task.get('success')
        self.__exception = task.get('exception')
        self.__terminated = task.get('terminated')

    def wait(self):
        if self.__terminated:
            return self.success
        m = self.client.wait(self.id)
        return m.get('success')
