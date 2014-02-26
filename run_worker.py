#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

from carotte import Worker


def get_website(url):
    r = urlopen(url)
    return r.status


def addition(*args):
    r = 0
    for i in args:
        r += i
    return r


if __name__ == "__main__":
    s = Worker()
    s.add_task('addition', addition)
    s.add_task('get_website', get_website)
    try:
        s.run()
    except KeyboardInterrupt:
        s.stop()
