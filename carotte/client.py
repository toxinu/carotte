#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import json
import base64
import pickle

from .task import Task


class Client(object):
    def __init__(self, workers=["tcp://localhost:5550"]):
        self.workers = workers
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        for address in self.workers:
            print('[client] Connecting to %s ...' % address)
            self.socket.connect(address)

    def run_task(self, task_name, task_args=[], task_kwargs={}):
        data = {
            'action': 'run_task',
            'name': task_name,
            'args': base64.b64encode(pickle.dumps(task_args)).decode('utf-8'),
            'kwargs': base64.b64encode(pickle.dumps(task_kwargs)).decode('utf-8')}
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        task = self.deserialize_task(msg)
        return task

    def deserialize_task(self, raw_data):
        data = json.loads(raw_data)
        task = Task(data.get('id'), data.get('name'), client=self)
        task.deserialize(raw_data)
        return task

    def get_task_result(self, task_id):
        data = {
            'action': 'get_result',
            'id': task_id
        }
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        return json.loads(msg)

    def wait(self, task_id):
        data = {
            'action': 'wait',
            'id': task_id
        }
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        return json.loads(msg)
