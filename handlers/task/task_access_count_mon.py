# coding=utf-8

import logging

from tornado.httpclient import AsyncHTTPClient
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen


request_log = logging.getLogger('request')


class Mon_Ip_Task(tornado.ioloop.PeriodicCallback):
    def __init__(self, application, callback_time):
        super(Mon_Ip_Task, self).__init__(self.post, callback_time)
        self.application = application

    @tornado.gen.coroutine
    def post(self):
        url = "http://{0}/access_count_mon/".format(self.application.url)
        http_client = AsyncHTTPClient()
        yield http_client.fetch(url,method="GET",request_timeout=120)



