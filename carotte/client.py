# -*- coding: utf-8 -*-
import zmq

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
        :param dict task_kwargs: (optional) Dict of keyword arguments
                                 to give to task

        :returns: :class:`carotte.Task` object

        """
        data = {
            'action': 'run_task',
            'name': task_name,
            'args': task_args,
            'kwargs': task_kwargs}
        self.socket.send_pyobj(data)
        task = self.socket.recv_pyobj()
        task.client = self
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
        self.socket.send_pyobj(data)
        task = self.socket.recv_pyobj()
        return task

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
        self.socket.send_pyobj(data)
        task = self.socket.recv_pyobj()
        return task
