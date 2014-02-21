#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import json


class Client(object):
    def __init__(self, port=5556):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:%s" % self.port)

    def run_task(self, task_name, task_args=[], task_kwargs={}):
        data = {
            'action': 'run_task',
            'task_name': task_name,
            'args': task_args,
            'kwargs': task_kwargs}
        self.socket.send_string(json.dumps(data))
        msg = self.socket.recv()
        msg = json.loads(msg.decode('utf-8'))
        return msg.get('task_id')

    def get_task_result(self, task_id):
        data = {
            'action': 'get_result',
            'task_id': task_id
        }
        self.socket.send_string(json.dumps(data))
        msg = self.socket.recv()
        msg = json.loads(msg.decode('utf-8'))
        return msg
