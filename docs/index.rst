Carotte
=======

Carotte is a lightweigth Celery for asynchronous tasks.

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

Install
-------

::

    pip install carotte

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   client
   worker
   task

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

