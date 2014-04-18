# -*- coding: utf-8 -*-
import zmq

from . import logger

__all__ = ['Client']


class Client(object):
    """
    :class:`carotte.Client` can send task and manage it.

    :param list worker: Worker address
    :param int timeout: Socket timeout
    :param boolean reconnect: Auto reconnect socket

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
    def __init__(self, worker="tcp://localhost:5550", timeout=10, reconnect=True):
        self.worker = worker
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.timeout = timeout
        self.reconnect = reconnect

        logger.info('Connecting to %s ...' % self.worker)
        self.socket.connect(self.worker)

    def __connect_socket(self):
        logger.info('Reconnecting to %s ...' % self.worker)
        self.socket.connect(self.worker)

    def __send_pyobj(self, data):
        try:
            self.socket.send_pyobj(data)
        except zmq.error.ZMQError:
            if self.reconnect:
                self.__connect_socket()
            else:
                raise

    def __recv_pyobj(self, notimeout=False):
        if notimeout or self.poller.poll(self.timeout * 1000):
            r = self.socket.recv_pyobj()
            if not r.get('success', False):
                exception = r.get('exception', Exception('Unhandler exception'))
                raise exception
            return r.get('task')
        else:
            raise IOError('Socket timeout (%s)' % self.worker)

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
        self.__send_pyobj(data)
        task = self.__recv_pyobj()
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
        self.__send_pyobj(data)
        task = self.__recv_pyobj()
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
        self.__send_pyobj(data)
        task = self.__recv_pyobj(notimeout=True)
        return task
