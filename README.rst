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
        return 'Hello %s!' % name

Run your worker (default on "tcp://127.0.0.1:5550"): ::

    carotte worker --tasks-module tasks

Run your client: ::

    >>> from carotte import Client
    >>> client = Client()
    >>> task = client.run_task('hello_world', ['foo'])
    >>> task.success
    >>> True
    >>> task.result
    >>> 'Hello foo!'

Scheduled tasks
---------------

Carotte is not a scheduler, its an asynchronous tasks runner.
But you can really set up scheduled tasks with schedule_.

Your ``tasks.py``: ::

    import requests
    from carotte import task

    @task
    def get(url):
        r = requests.get(url)
        if r.status_code != 200:
            # Do stuff
            return False
        return True

Your ``scheduler.py``: ::
    
    import time
    import schedule
    from carotte import client

    client = Client()
    schedule.every(10).seconds.do(client.run_task, 'get', ['http://google.com'])

    while True:
        schedule.run_pending()
        time.sleep(1)

Run your worker and your scheduler: ::

    carotte worker --tasks-module tasks
    # In another terminal
    python scheduler.py

.. _schedule: https://github.com/dbader/schedule
