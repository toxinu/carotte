# -*- coding: utf-8 -*-
import sys
import zmq
import uuid
import time
import threading

try:
    import queue
except ImportError:
    import Queue as queue

from . import Task
from . import logger

__all__ = ['Worker']


class Worker(object):
    """
    :class:`carotte.Worker` register and wait task to run.

    :param string bind: Address to bind
    :param int thread: Number of thread

    >>> from carotte import Worker
    >>> worker = Worker(thread=10)
    >>> worker.add_task('hello', lambda: 'hello world')
    >>> worker.run()

    """
    def __init__(self, bind="tcp://127.0.0.1:5550", thread=1):
        self.thread = thread
        self.bind = bind
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.tasks = {}
        self.task_results = {}

        self.lock = threading.Lock()

        self.queue = queue.Queue()
        logger.info('Running %s thread(s)...' % self.thread)
        for i in range(int(self.thread)):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()

    def run(self):
        """
        Blocking method that run the server.
        """
        if self.tasks:
            logger.info('Registered tasks: %s' % ', '.join(self.tasks))
        else:
            logger.info('No tasks registered')
        logger.info('Listening on %s ...' % self.bind)
        self.socket.bind(self.bind)

        while True:
            msg = self.socket.recv_pyobj()

            action = msg.get('action')
            if action == 'run_task':
                task = Task(str(uuid.uuid4()), msg.get('name'), [], {})

                if msg.get('args'):
                    task.args = msg.get('args', [])
                if msg.get('kwargs'):
                    task.kwargs = msg.get('kwargs', {})

                self.task_results[task.id] = task
                self.queue.put(task.id)
                self.socket.send_pyobj(task)
            elif action == 'get_result':
                task_id = msg.get('id')
                task = self.task_results.get(task_id)
                if task:
                    response = task
                else:
                    response = {'id': task_id, 'error': 'task not found'}
                self.socket.send_pyobj(response)
            elif action == 'wait':
                task_id = msg.get('id')
                task = self.task_results[task_id]
                if task:
                    while not task.terminated:
                        task = self.task_results[task_id]
                        time.sleep(1)
                    response = task
                else:
                    response = {'id': task_id, 'error': 'task not found'}
                self.socket.send_pyobj(response)
            else:
                response = {'success': False, 'error': 'Message malformed'}
                self.socket.send_pyobj(response)

    def add_task(self, task_name, task):
        """
        Register a task to server.

        :param string task_name: Task name used by clients
        :param method task: Method that will be called
        """
        self.tasks[task_name] = task

    def delete_task(self, task_name):
        """
        Unregister a task from server.

        :param string task_name: Task name
        """
        del(self.tasks[task_name])

    def _worker(self):
        while True:
            task_id = self.queue.get()
            task_name = self.task_results[task_id].name
            task_args = self.task_results[task_id].args
            task_kwargs = self.task_results[task_id].kwargs

            with self.lock:
                logger.info('Running %s (args:%s) (kwargs:%s)' % (
                    task_name, task_args, task_kwargs))
            task = self.tasks.get(task_name)

            try:
                self.task_results[task_id].set_result(task(
                    *task_args, **task_kwargs))
                self.task_results[task_id].set_success(True)
            except Exception as err:
                self.task_results[task_id].set_exception("%s" % err)

            self.task_results[task_id].set_terminated(True)
            logger.info('Finished task %s (success: %s)' % (
                task_id, self.task_results[task_id].success))
            self.queue.task_done()

    def stop(self):
        """
        Stop server and all its threads.
        """
        logger.info('Waiting tasks to finish...')
        self.queue.join()
        self.socket.close()
        logger.info('Exiting...')
        sys.exit(0)
