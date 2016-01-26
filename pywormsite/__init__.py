import os

import redis
import yaml


def config():
    return yaml.load(
        open(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/config.yaml', 'r',
             encoding='utf8'))


class RedisDriver:
    def __init__(self):

        self.config = config()
        self.host = self.config["pyworm_blog"]["host"]
        self.port = 6379

        self._master_13 = None  #其他
        self._master_14 = None  #存储所有IP
        self._master_15 = None  #统计在线人数

    @property
    def master_13(self):
        if self._master_13 is None:
            self._master_13 = redis.StrictRedis(host=self.host, port=self.port, db=13, decode_responses=True)
        return self._master_13

    @property
    def master_14(self):
        if self._master_14 is None:
            self._master_14 = redis.StrictRedis(host=self.host, port=self.port, db=14, decode_responses=True)
        return self._master_14

    @property
    def master_15(self):
        if self._master_15 is None:
            self._master_15 = redis.StrictRedis(host=self.host, port=self.port, db=15, decode_responses=True)
        return self._master_15


# master_13 = RedisDriver().master_13
# master_13.set("hello","world")
# a = master_13.get("hello")
# print(a)
