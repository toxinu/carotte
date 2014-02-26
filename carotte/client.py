# -*- coding: utf-8 -*-
import zmq
import json
import base64
import pickle

from . import Task
from . import logger

__all__ = ['Client']


class Client(object):
    """
    :class:`carotte.Client` can send task and manage it.

    :param list workers: List of worker addresses

    >>> from carotte import Client
    >>> client = Client()
    >>> task = client.run_task('hello')
    >>> task.terminated
    >>> False
    >>> task.wait()
    >>> task.terminated
    >>> True
    >>> task.result
    >>> 'hello world'
    """
    def __init__(self, workers=["tcp://localhost:5550"]):
        self.workers = workers
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        for address in self.workers:
            logger.info('Connecting to %s ...' % address)
            self.socket.connect(address)

    def run_task(self, task_name, task_args=[], task_kwargs={}):
        """
        Run asynchronous task on a :class:`carotte.Worker`.

        :param string task_name: Name of task to execute
        :param list task_args: (optional) List of arguments to give to task
        :param dict task_kwargs: (optional) Dict of keyword arguments to give to task

        :returns: :class:`carotte.Task` object

        """
        data = {
            'action': 'run_task',
            'name': task_name,
            'args': base64.b64encode(pickle.dumps(task_args)).decode('utf-8'),
            'kwargs': base64.b64encode(pickle.dumps(task_kwargs)).decode('utf-8')}
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        task = self._deserialize_task(msg)
        return task

    def _deserialize_task(self, raw_data):
        """
        Deserialize and create a :class:`carotte.Task` object from raw data.

        :param string raw_data: Raw data which contain a task in json

        :returns: :class:`carotte.Task` object
        """
        data = json.loads(raw_data)
        task = Task(data.get('id'), data.get('name'), client=self)
        task._deserialize(raw_data)
        return task

    def get_task_result(self, task_id):
        """
        Get task result from worker. If the task is not finished, return None.
        It's prefered to use :class:`carotte.Task` object directly.

        :param string task_id: Task ID

        :returns: Task dict
        :rtype: dict
        """
        data = {
            'action': 'get_result',
            'id': task_id
        }
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        return json.loads(msg)

    def wait(self, task_id):
        """
        Blocking method which wait end of task.
        It's prefered to use :class:`carotte.Task` object directly

        :param string task_id: Task ID

        :returns: Task dict
        :rtype: dict
        """
        data = {
            'action': 'wait',
            'id': task_id
        }
        self.socket.send_json(data)
        msg = self.socket.recv_json()
        return json.loads(msg)
