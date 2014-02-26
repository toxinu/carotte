Carotte
=======

Carotte is a very lightweight Celery.

Install
-------

::

    git clone https://github.com/socketubs/carotte.git
    cd carotte
    virtualenv virtenv
    source virtenv/bin/activate
    pip install -r requirements.txt


Getting started
---------------

::

    python run_worker.py
    python run_client.py


More
----

::

    >>> from carotte import Worker
    >>> worker = Worker()
    >>> worker.add_task('hello', lambda: 'hello world')
    >>> c.run()

::

    >>> from carotte import Client
    >>> client = Client()
    >>> task = client.run_task('hello')
    >>> task.success
    >>> True
    >>> task.result
    >>> 'hello world'
