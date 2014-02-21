#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import zmq
import uuid
import json
import time
import threading
from queue import Queue


class Server(object):
    def __init__(self, port=5556):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)
        self.tasks = {}
        self.task_results = {}

        self.lock = threading.Lock()

        self.queue = Queue()
        for i in range(4):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def run(self):
        while True:
            # Retrieving message
            msg = self.socket.recv()
            msg = json.loads(msg.decode('utf-8'))

            action = msg.get('action')
            if action == 'run_task':
                msg['task_id'] = "%s" % uuid.uuid4()

                # Send task to queue
                self.queue.put(msg)

                # Response ack
                response = {
                    'task_name': msg.get('task_name'),
                    'state': 'running',
                    'task_id': msg.get('task_id')}
            elif action == 'get_result':
                task_id = msg.get('task_id')
                task = self.task_results.get(task_id)
                if task:
                    response = {'task_id': task_id}
                    response.update(task)
                else:
                    response = {'task_id': task_id, 'error': 'task not found'}

            self.socket.send_string(json.dumps(response))

    def add_task(self, task_name, task):
        self.tasks[task_name] = task

    def del_task(self, task_name):
        del(self.tasks[task_name])

    def worker(self):
        while True:
            item = self.queue.get()
            task_id = item.get('task_id')
            task_name = item.get('task_name')
            task_args = item.get('args', [])
            task_kwargs = item.get('kwargs', {})

            self.task_results[task_id] = {}
            self.task_results[task_id]['task_id'] = task_id
            self.task_results[task_id]['task_name'] = task_name
            self.task_results[task_id]['task_args'] = task_args
            self.task_results[task_id]['task_kwargs'] = task_kwargs
            self.task_results[task_id]['task_result'] = None
            self.task_results[task_id]['task_success'] = None
            self.task_results[task_id]['task_exception'] = None
            with self.lock:
                print('[task] Running %s (args:%s) (kwargs:%s)' % (
                    task_name, task_args, task_kwargs))
            task = self.tasks.get(task_name)

            try:
                self.task_results[task_id]['task_result'] = task(
                    *task_args, **task_kwargs)
                self.task_results[task_id]['task_success'] = True
            except Exception as err:
                self.task_results[task_id]['task_exception'] = "%s" % err

            self.queue.task_done()

    def stop(self):
        self.queue.join()
        sys.exit(0)


def addition(*args):
    time.sleep(5)
    r = 0
    for n in args:
        r += n
    return r


if __name__ == "__main__":
    s = Server()
    s.add_task('addition', addition)
    try:
        s.run()
    except KeyboardInterrupt:
        s.stop()
