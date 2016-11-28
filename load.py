import dictionary


def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Dictionary(object):
    def __init__(self, x=0):
        self.dic = dictionary.dic
    def getDic(self):
        return self.dic

