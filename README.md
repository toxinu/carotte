Carotte
=======

Carotte is a very lightweight Celery.

Install
-------

    git clone https://github.com/socketubs/carotte.git
    cd carotte
    virtualenv virtenv
    source virtenv/bin/activate
    pip install -r requirements.txt


Getting started
---------------

    python run_worker.py
    python run_client.py


More
----

**Worker**

    >>> from carotte.worker import Worker
    >>> worker = Worker(thread=10)
    >>>
    >>> import time
    >>> def hello(who):
    >>>     time.sleep(1)
    >>>     return 'Hello %s!' % who
    >>>
    >>> worker.add_task('hello', hello)
    >>> worker.run()

**Client**

    >>> from carotte.client import Client
    >>> client = Client()
    >>> [client] Connecting to tcp://localhost:5550 ...
    >>> task = client.run_task('hello', ['carotte'])
    >>> task.wait()
    >>> task.success
    >>> True
    >>> task.result
    >>> 'Hello carotte!'
