# -*- coding: utf-8 -*-


class Task(object):
    """
    :class: `Task` can retrieve it state from worker and by managed from client.
    Never create a task from nothing, a task is mostly create by :class:`carotte.Client`.

    :param int id: Task ID
    :param string name: Task name
    :param array args: (optional) Task arguments
    :param dict kwargs: (optional) Task keyword arguments
    :param client: :class:`carotte.Client` object
    """
    def __init__(self, id, name, args=[], kwargs={}, client=None):
        self.id = id
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.__terminated = False
        self.__terminated_at = None
        self.__result = None
        self.__success = None
        self.__exception = None

        self.client = client

    @property
    def result(self):
        if self.__terminated:
            return self.__result
        self.__update_task()
        return self.__result

    @property
    def success(self):
        if self.__terminated:
            return self.__success
        self.__update_task()
        return self.__success

    @property
    def exception(self):
        if self.__terminated:
            return self.__exception
        self.__update_task()
        return self.__exception

    @property
    def terminated(self):
        if self.__terminated:
            return self.__terminated
        self.__update_task()
        return self.__terminated

    @property
    def terminated_at(self):
        if self.__terminated:
            return self.__terminated_at
        self.__update_task()
        return self.__terminated_at

    def set_result(self, result):
        self.__result = result

    def set_success(self, success):
        self.__success = success

    def set_exception(self, exception):
        self.__exception = exception

    def set_terminated(self, terminated):
        self.__terminated = terminated

    def set_terminated_at(self, terminated_at):
        self.__terminated_at = terminated_at

    def __update_task(self, task=None):
        if self.client is None:
            return
        if task is None:
            task = self.client.get_task_result(self.id)
        self.__result = task.result
        self.__success = task.success
        self.__exception = task.exception
        self.__terminated = task.terminated
        self.__terminated_at = task.terminated_at

    def wait(self):
        if self.__terminated:
            return self.success
        task = self.client.wait(self.id)
        self.__update_task(task=task)
        return self.success
