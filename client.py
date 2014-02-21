#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import json

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)

for i in range(0, 50):
    data = {'action': 'run_task', 'task_name': 'addition', 'args': [1, 2, 3, 10, i]}
    socket.send_string(json.dumps(data))
    msg = socket.recv()
    print(msg)
