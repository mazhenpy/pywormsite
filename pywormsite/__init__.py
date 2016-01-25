import redis
import tornado
import tornado.web

class RedisDriver(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(RedisDriver, self).__init__(application, request)

        self.host = self.application.host
        self.port = 6379

        self._master_13 = None
        self._master_14 = None
        self._master_15 = None

    @property
    def master_13(self):
        if self._master_13 is None:
            self._master_13 = redis.StrictRedis(host=self.host, port=self.port, db=13)
        return self._master_13

    @property
    def master_14(self):
        if self._master_14 is None:
            self._master_14 = redis.StrictRedis(host=self.host, port=self.port, db=14)
        return self._master_14

    @property
    def master_15(self):
        if self._master_15 is None:
            self._master_15 = redis.StrictRedis(host=self.host, port=self.port, db=15)
        return self._master_15