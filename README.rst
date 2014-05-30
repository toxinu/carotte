Carotte
=======

Carotte is a very lightweight Celery on zmq.

Install
-------

::

    pip install carotte


Getting started
---------------

Create your ``app.py``: ::

    from carotte import Carotte

    my_app = Carotte()

    @my_app.task
    def hello_world(name):
        return 'Hello %s!' % name

Run your worker (default on "tcp://127.0.0.1:5550"): ::

    carotte worker --app app:my_app

Run tasks: ::

    >>> from app import hello_world
    >>> t = hello_world.delay(['Carotte'])
    >>> t.success
    >>> True
    >>> t.result
    >>> 'Hello Carotte!'

Or run a client (if don't have tasks on your system): ::

    >>> from carotte import Client
    >>> client = Client()
    >>> task = client.run_task('hello_world', ['Carotte'])
    >>> task.success
    >>> True
    >>> task.result
    >>> 'Hello Carotte!'

Scheduled tasks
---------------

Carotte is not a scheduler, its an asynchronous tasks runner.
But you can really set up scheduled tasks with schedule_.

Your ``app.py``: ::

    import requests
    from carotte import Carotte

    my_app = Carotte()

    @app.task
    def get(url):
        r = requests.get(url)
        if r.status_code != 200:
            # Do stuff
            return False
        return True

Your ``scheduler.py``: ::

    import time
    import schedule
    from app import get

    schedule.every(10).seconds.do(get, 'http://google.com')

    while True:
        schedule.run_pending()
        time.sleep(1)

Run your worker and your scheduler: ::

    carotte worker --app app:my_app
    python scheduler.py

.. _schedule: https://github.com/dbader/schedule
