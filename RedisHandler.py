import redis
import json

class RedisHandler:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_new_id(self):
        new_id = len(list(self.redis.scan_iter('task_*')))
        return 'task_'+str(new_id)

    def add_new_task(self, qid, data):
        self.redis.set(qid, json.dumps(data))

    def get_task_by_id(self, id):
        data = self.redis.get('task_'+str(id))
        if not data:
            return False
        return json.loads(data)
