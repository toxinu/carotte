# -*- coding: utf-8 -*-


class Base(object):
    def add_task(self, task):
        raise NotImplemented()

    def delete_task(self, task):
        raise NotImplemented()

    def update_task(self, task):
        raise NotImplemented()

    def get_task(self, task_id):
        raise NotImplemented()

    def cleanup(self, task_result_expires):
        raise NotImplemented()
