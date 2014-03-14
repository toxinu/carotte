# -*- coding: utf-8 -*-
import pickle
from datetime import datetime

from . import Base


class Redis(Base):
    def __init__(self, host='localhost', port=6379, db=0):
        import redis
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def add_task(self, task):
        self.r.set('task_%s' % task.id, pickle.dumps(task))

    def delete_task(self, task):
        self.r.delete('task_%s' % task.id)

    def update_task(self, task):
        self.r.set('task_%s' % task.id, pickle.dumps(task))

    def get_task(self, task_id):
        return pickle.loads(self.r.get('task_%s' % task_id))

    def cleanup(self, task_result_expires):
        now = datetime.now()
        stats = {'count': 0}
        for key in self.r.keys('task_*'):
            result = self.get_task(key.replace('task_', ''))
            if result.terminated:
                if result.terminated_at < (now - task_result_expires):
                    stats['count'] += 1
                    self.delete_task(result)
        return stats
