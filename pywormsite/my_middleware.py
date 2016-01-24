# coding:utf-8
import logging
import time

from django.core.cache import cache


request_log = logging.getLogger('request')

# 创建cache命令: python manage.py createcachetable django_cache


class IPMiddleware(object):
    def process_request(self, request):

        #ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        # 统计在线人数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        #ip在cache中存储{"127.0.0.1":"2016-1-1 02:02"}
        check_ip = cache.get(ip, '')
        if not check_ip:
            cache.set(ip, time.strftime("%Y-%m-%d %H:%M", time.localtime()), 60 * 1)


        #ips_all[在线的ip] 在cache中存储{"ips_all":["127.0.0.1","127.0.0.1"]}
        #ips_all=["127.0.0.1","127.0.0.1"]
        #ips_all为所有的不重复的ip列表
        #ips_to_sql需要同步到数据库的ip
        ips_to_sql = cache.get("ips_to_sql", [])
        ips_all = cache.get("ips_all", [])
        if ip not in ips_all:
            ips_to_sql.append(ip)
            ips_all.append(ip)
            cache.set("ips_to_sql", ips_to_sql)
            cache.set("ips_all", ips_all)


        # online_num = 0
        # if ips_all:
        # online_ip_dict = cache.get_many(ips_all).keys() #dict_keys(['127.0.0.1','127.0.0.1'])
            # cache.get_many(['127.0.0.1', '127.0.0.2', '127.0.0.3']) {'127.0.0.1': '2016-1-1 02:02', '127.0.0.2': '2016-1-1 02:02', '127.0.0.3': '2016-1-1 02:02'}  返回未超时的所有键值。
        # online_num = len(online_ip_dict)
        #request_log.info("当前在线人数:{0}".format(online_num))




        #最近访问
        #ips_access[所有进来的ip列表,ip不重复且最大值为5]在cache中存储{"ips_access":["127.0.0.1","127.0.0.1"]} ips_access=["127.0.0.1","127.0.0.1"]
        ips_access = cache.get("ips_access", [])
        if ip not in ips_access:
            ips_access.append(ip)
            if len(ips_access) > 5:
                ips_access.pop(0)
            cache.set("ips_access", ips_access)


        self.clicks(ip)


    # 统计PV，IP访问量
    def clicks(self, ip):
        mon = time.strftime('%Y-%m', time.localtime(time.time()))
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        #ips_mon[一个月的所有ip]
        #access_mon[一个月的点击量]
        access_mon = cache.get(mon, {'IP': 0, 'PV': 0})
        access_mon['PV'] += 1
        ips_mon = cache.get("ips_mon_{0}".format(mon), [])
        if ip not in ips_mon:
            ips_mon.append(ip)
            access_mon['IP'] += 1
            cache.set("ips_mon_{0}".format(mon), ips_mon, 60 * 60 * 24 * 60)
        cache.set(mon, access_mon, 60 * 60 * 24 * 60)

        access_day = cache.get(day, {'IP': 0, 'PV': 0})
        access_day['PV'] += 1
        ips_day = cache.get("ips_day_{0}".format(day), [])
        if ip not in ips_day:
            ips_day.append(ip)
            access_day['IP'] += 1
            cache.set("ips_day_{0}".format(day), ips_day, 60 * 60 * 24 * 2)
        cache.set(day, access_day, 60 * 60 * 24 * 2)

        # access_mon = cache.get(mon, {'IP': 0, 'PV': 0})
        # access_day = cache.get(day, {'IP': 0, 'PV': 0})
        # print(access_mon, access_day)





