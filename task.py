import itertools


class Task:
    id_iter = itertools.count()
    name: str
    status: bool

    def __init__(self, name, status):
        self.id = next(Task.id_iter)
        self.name = name
        self.status = status


    def __str__(self):
        return '{{ \"name\": {} , \"status\": {}, \"id\":{} }} '.format(self.name, self.status, self.id)
