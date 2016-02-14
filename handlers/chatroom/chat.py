# coding:utf-8
import logging

import tornado
import tornado.web
import tornado.gen
import tornado.escape
import tornado.websocket
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient


request_log = logging.getLogger('request')
chat_log = logging.getLogger('chat')
error_log = logging.getLogger('chat')

@tornado.gen.coroutine
def sina_ip(ip):
    attribution = ""
    if ip == "127.0.0.1":
        ip = '183.208.22.171'
    if len(ip)>20:
        ip = '183.208.22.171'
    http_client = AsyncHTTPClient()
    response = None
    url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip={0}".format(ip)
    try:
        response = yield http_client.fetch(url, method='GET', request_timeout=120)
    except Exception as e:
        error_log.info(e)

    if response and response.code == 200:
        response_body = eval(response.body.decode('utf8')[21:-1])
        try:
            province = response_body['province']
            city = response_body['city']
            attribution = province + city
        except Exception as e:
            error_log.error(e)

    ip_piece = ip.split(".")
    ip_piece[1] = '*'
    ip_piece[2] = '*'
    ip_attribution = '.'.join(ip_piece) + '[' + attribution + ']'

    return ip_attribution



class ChatHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        client = self.request.headers['user-agent']
        url = "http://{0}/online_ips/".format(self.application.url)
        online_ips = 1
        try:
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch(url, method='GET', request_timeout=120)
            online_ips = response.body.decode()
        except Exception as e:
            error_log.error(e)

        ip = self.request.remote_ip
        attribution = yield sina_ip(ip)
        if not attribution:
            attribution = '未知地'
        chat_log.info("{0}-To-Chatroom".format(attribution))
        self.render('chat.html', attribution=attribution, client=client, online_ips=online_ips,
                    messages=ChatSocketHandler.cache)




class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200
    def __init__(self,application, request):
        super(ChatSocketHandler, self).__init__(application, request)
        self.ip = self.request.remote_ip

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        #print("new client opened")
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
        #request_log.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    @tornado.gen.coroutine
    def on_message(self, message):
        self.attribution = yield sina_ip(self.ip)
        chat_log.info("{0}-Send-Message-{1}".format(self.attribution,message))
        ChatSocketHandler.send_updates(message)




