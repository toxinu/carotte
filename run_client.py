#!/usr/bin/env python
# -*- coding: utf-8 -*-
from carotte.client import Client


if __name__ == "__main__":
    c = Client()
    # Send 10 tasks
    tasks = []
    for i in range(0, 50):
        t = c.run_task('get_website', ['http://socketubs.org'])
        tasks.append(t)

    for t in tasks:
        #t.wait()
        print(t.result)

    # # Send 5 another tasks but wait for it
    # for t in range(0, 4):
    #     i = c.run_task('get_website', ['http://socketubs.org'])
    #     print('Task_id: %s' % i)
    #     print(c.wait(i.id))
