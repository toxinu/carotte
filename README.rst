Carotte
=======

Carotte is a very lightweight Celery on zmq.

Install
-------

::

    pip install carotte


Getting started
---------------

Create your ``tasks.py``: ::

    from carotte import task

    @task
    def hello_world(name):
        return 'Hello %s!'' % name

Run your worker: ::

    carotte --tasks-module tasks.py

Run your client: ::

    >>> from carotte import Client
    >>> client = Client()
    >>> task = client.run_task('hello_world', ['foo'])
    >>> task.success
    >>> True
    >>> task.result
    >>> 'Hello foo!'
