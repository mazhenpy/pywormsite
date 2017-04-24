# -*- coding: utf-8 -*-
import json
import os
import sys

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
from tornado.httpclient import AsyncHTTPClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


def show_logo():
    print('''
 WELCOME TO MY WEBSITE
(C) 2015-2016, Pyworm Blog''')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/websocket', ChatSocketHandler),
        ]

        settings = {
            "template_path": os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                "templates"),
            "static_path": os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                "static"),
            "upload_path": os.path.join(
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                "uploads"),
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False,
            "debug": False,
        }
        self.port = '10022'

        tornado.web.Application.__init__(self, handlers, **settings)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    @tornado.gen.coroutine
    def get(self):
        print ('handling...')
        self.finish('hollo world')
        return

    def check_origin(self, origin):
        return True

    def __init__(self, application, request):
        super(ChatSocketHandler, self).__init__(application, request)
        self.ip = self.request.remote_ip

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                pass

    @tornado.gen.coroutine
    def on_message(self, message):
        self.attribution = yield sina_ip(self.ip)
        data = {"attr": self.attribution, "msg": message}
        data = json.dumps(data)
        ChatSocketHandler.send_updates(data)


@tornado.gen.coroutine
def sina_ip(ip):
    attribution = ""
    if ip == "127.0.0.1":
        ip = '183.208.22.171'
    if len(ip) > 20:
        ip = '183.208.22.171'
    http_client = AsyncHTTPClient()
    response = None
    url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip={0}".format(ip)
    try:
        response = yield http_client.fetch(url, method='GET', request_timeout=120)
    except Exception as e:
        pass

    if response and response.code == 200:
        response_body = eval(response.body.decode('utf8')[21:-1])
        try:
            province = response_body['province']
            city = response_body['city']
            attribution = province + city
        except Exception as e:
            pass

    ip_piece = ip.split(".")
    ip_piece[1] = '*'
    ip_piece[2] = '*'
    ip_attribution = '.'.join(ip_piece) + '[' + attribution + ']'

    return ip_attribution


if __name__ == '__main__':
    application = Application()
    show_logo()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(application.port)
    tornado.ioloop.IOLoop.instance().start()
