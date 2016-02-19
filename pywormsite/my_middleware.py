# coding:utf-8
import logging
import time

from django.core.cache import cache

from pywormsite import RedisDriver


request_log = logging.getLogger('request')

# 创建cache命令: python manage.py createcachetable django_cache


class IPMiddleware(object):
    def __init__(self):
        self.master_13 = RedisDriver().master_13
        self.master_14 = RedisDriver().master_14
        self.master_15 = RedisDriver().master_15

    def process_request(self, request):
        # ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        user_agent = request.META.get('HTTP_USER_AGENT', "")
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.master_13.set("user_agent_set:{0}".format(day), user_agent)

        spider = False
        spider_list = ["Spider", "spider", "Googlebot", "bingbot"]
        for i in spider_list:
            if i in user_agent:
                spider = True
                break

        if len(ip) < 20:
            if not spider:

                # ip = "183.206.160.95"

                # ip:给每个ip存储过期时间
                #“online_ips_str”:当前在线人数
                #“all_ips_set”:所有不重复IP集合
                #“lately_ip_list” "lately_ip_set"

                #更新ip访问时间
                self.master_14.set(ip, time.strftime("%Y-%m-%d %H:%M", time.localtime()))

                # 统计在线人数
                self.master_15.setex("online_ips_str:{0}".format(ip), 60 * 1,
                                     time.strftime("%Y-%m-%d %H:%M", time.localtime()))
                online_ips = self.master_15.dbsize()

                #存储所有IP
                if not self.master_13.sismember("all_ips_set", ip):
                    self.master_13.sadd("all_ips_set", ip)
                    self.master_13.lpush("all_ips_list", ip)

                #最近访问
                #ips_access[所有进来的ip列表,ip不重复且最大值为5]在cache中存储{"ips_access":["127.0.0.1","127.0.0.1"]} ips_access=["127.0.0.1","127.0.0.1"]
                ips_access = cache.get("ips_access", [])
                if ip not in ips_access:
                    ips_access.append(ip)
                    if len(ips_access) > 5:
                        ips_access.pop(0)
                    cache.set("ips_access", ips_access, 60 * 60 * 24 * 30)

                self.clicks(ip)


    # 统计PV，IP访问量
    def clicks(self, ip):
        mon = time.strftime('%Y-%m', time.localtime(time.time()))
        m = 'Month:{0}'.format(mon)

        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        d = 'Day:{0}'.format(day)

        self.master_13.hincrby(d, 'PV')
        self.master_13.hincrby(m, 'PV')

        self.master_13.sadd('all_mon_set:month', mon)  # 一共统计了哪几个月
        self.master_13.sadd('all_day_set:day', day)  # 一共统计了哪几个日子

        # 一个月的所有ip
        if not self.master_13.sismember("mon_ip_set:{0}".format(mon), ip):
            self.master_13.sadd("mon_ip_set:{0}".format(mon), ip)
            self.master_13.hincrby(m, 'IP')

            #self.master_13.hget(m, 'IP')

        #一天的所有ip
        if not self.master_13.sismember("day_ip_set:{0}".format(day), ip):
            self.master_13.sadd("day_ip_set:{0}".format(day), ip)
            self.master_13.hincrby(d, 'IP')


