# -*- coding: utf-8 -*-
import os
import sys

import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.gen
from tornado.web import url

from pywormsite import config


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from handlers.chatroom.chat import ChatHandler, ChatSocketHandler
from handlers.search_blog import SearchHandler
from handlers.task.task_access_count_day import Day_Ip_Task
from handlers.task.task_access_count_mon import Mon_Ip_Task
from handlers.task.task_access_ips import Total_Ip_Task


def show_logo():
    print('''
 WELCOME TO MY WEBSITE
(C) 2015-2016, Pyworm Blog''')


def show_index(ip, port):
    print('''
******************************************************************
*网站主页：http://{ip}:{port}/
*后台管理：http://{ip}:{port}/admin/
*将博客转存数据库：http://{ip}:{port}/blog/to_mysql/
*生成搜索目录： http://{ip}:{port}/catalog
*网络聊天室： http://{ip}:{port}/chat
*将IP归属地同步数据库：http://{ip}:{port}/access_ip/
*将月访问量同步数据库：http://{ip}:{port}/access_count_mon/
*将日访问量同步数据库：http://{ip}:{port}/access_count_day/
******************************************************************
    '''.format(ip=ip, port=port))


if django.VERSION[1] > 5:
    print("DJANGO_VERSION:", django.VERSION)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()


class Application(tornado.web.Application):
    def __init__(self):
        wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())

        self.config = config()

        self.host = self.config["pyworm_blog"]["host"]
        self.port = self.config["pyworm_blog"]["port"]
        self.url = self.config["pyworm_blog"]["url"]

        handlers = [
            ('/chat', ChatHandler),
            ('/websocket', ChatSocketHandler),
            ('/search_blog', SearchHandler),  # 博客搜索

            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
            # url(r"/uploads/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path'),
            # #("/uploads", tornado.web.StaticFileHandler),
        ]

        settings = {
            "template_path": os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                                          "templates"),
            "static_path": os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                                        "static"),
            "upload_path": os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)),
                                        "uploads"),
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False,
            "debug": False,
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    application = Application()
    show_logo()
    show_index(application.host, application.port)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(application.port)
    Day_Ip_Task(application, 1000 * 60 * 60 * 24).start()
    Mon_Ip_Task(application, 1000 * 60 * 60 * 24 * 30).start()
    Total_Ip_Task(application, 1000 * 60 * 60 * 24).start()
    tornado.ioloop.IOLoop.instance().start()


