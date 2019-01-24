import redis
import json

'''Класс для работы с redis'''
class RedisHandler:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    '''Метод для получения крайнего незанятого ID'''
    def get_new_id(self):
        new_id = len(list(self.redis.scan_iter('task_*')))
        return 'task_'+str(new_id)

    '''Метод, добавляющий новое задание на ресайзинг'''
    def add_new_task(self, qid, data):
        self.redis.set(qid, json.dumps(data))

    '''Метод, возвращающий данные о задаче по ее ID'''
    def get_task_by_id(self, id):
        data = self.redis.get(id)
        if not data:
            return False
        return json.loads(data)
