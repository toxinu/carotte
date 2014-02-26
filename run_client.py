#!/usr/bin/env python
# -*- coding: utf-8 -*-
from carotte import Client


if __name__ == "__main__":
    c = Client()
    tasks = []
    print("Sending 10 tasks...")
    for i in range(0, 10):
        t = c.run_task('get_website', ['http://google.com'])
        tasks.append(t)

    print("Waiting for results...")
    for t in tasks:
        t.wait()
        print("task %s (%s)" % (t.id, t.result))
