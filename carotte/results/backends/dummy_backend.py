# -*- coding: utf-8 -*-
from datetime import datetime
from . import Base


class Dummy(Base):
    def __init__(self):
        self.results = {}

    def add_task(self, task):
        self.results[task.id] = task

    def delete_task(self, task):
        del self.results[task.id]

    def update_task(self, task):
        self.results[task.id] = task

    def get_task(self, task_id):
        return self.results.get(task_id)

    def cleanup(self, task_result_expires):
        now = datetime.now()
        stats = {'count': 0}
        for result in self.results.values():
            if result.terminated:
                if result.terminated_at < (now - task_result_expires):
                    stats['count'] += 1
                    self.delete_task(result)
        return stats
