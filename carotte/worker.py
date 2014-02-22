#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import zmq
import uuid
import time
import queue
import base64
import pickle
import threading

from .task import Task


class Worker(object):
    def __init__(self, bind="tcp://127.0.0.1:5550", thread=1):
        self.thread = thread
        self.bind = bind
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.tasks = {}
        self.task_results = {}

        self.lock = threading.Lock()

        self.queue = queue.Queue()
        for i in range(self.thread):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def run(self):
        print('[server] Registered tasks:')
        for task in self.tasks.keys():
            print('[server]   - %s' % task)

        print("[server] Listening on %s ..." % self.bind)
        self.socket.bind(self.bind)

        while True:
            msg = self.socket.recv_json()

            action = msg.get('action')
            if action == 'run_task':
                task = Task(str(uuid.uuid4()), msg.get('name'), [], {})

                if msg.get('args'):
                    task.args = pickle.loads(base64.b64decode(msg.get('args')))
                if msg.get('kwargs'):
                    task.kwargs = pickle.loads(base64.b64decode(msg.get('kwargs')))

                self.task_results[task.id] = task
                self.queue.put(task.id)
                response = task.serialize()
                self.socket.send_json(response)
            elif action == 'get_result':
                task_id = msg.get('id')
                task = self.task_results.get(task_id)
                if task:
                    response = task.serialize()
                else:
                    response = {'id': task_id, 'error': 'task not found'}
                self.socket.send_json(response)
            elif action == 'wait':
                task_id = msg.get('id')
                task = self.task_results[task_id]
                if task:
                    while not task.terminated:
                        task = self.task_results[task_id]
                        time.sleep(1)
                    response = task.serialize()
                else:
                    response = {'id': task_id, 'error': 'task not found'}
                self.socket.send_json(response)
            else:
                response = {'success': False, 'error': 'Message malformed'}
                self.socket.send_json(response)

    def add_task(self, task_name, task):
        self.tasks[task_name] = task

    def del_task(self, task_name):
        del(self.tasks[task_name])

    def worker(self):
        while True:
            task_id = self.queue.get()
            task_name = self.task_results[task_id].name
            task_args = self.task_results[task_id].args
            task_kwargs = self.task_results[task_id].kwargs

            with self.lock:
                print('[server] Running %s (args:%s) (kwargs:%s)' % (
                    task_name, task_args, task_kwargs))
            task = self.tasks.get(task_name)

            try:
                self.task_results[task_id].set_result(task(
                    *task_args, **task_kwargs))
                self.task_results[task_id].set_success(True)
            except Exception as err:
                self.task_results[task_id].set_exception("%s" % err)

            self.task_results[task_id].set_terminated(True)
            print('[server] Finished task %s (success: %s)' % (
                task_id, self.task_results[task_id].success))
            self.queue.task_done()

    def stop(self):
        print('[server] Waiting tasks to finish...')
        self.queue.join()
        print('[server] Exiting...')
        sys.exit(0)
