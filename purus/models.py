# coding:utf-8
from django.db import models


#月访问量
class Access_amount_mon(models.Model):
    access_time = models.CharField(u'访问时间',max_length=20, primary_key=True)
    access_ip = models.IntegerField(u'ip访问量')
    access_pv = models.IntegerField(u'网站点击访问量')

    def __unicode__(self):
        return self.access_time

#日访问量
class Access_amount_day(models.Model):
    access_time = models.CharField(u'访问时间',max_length=20, primary_key=True)
    access_ip = models.IntegerField(u'ip访问量')
    access_pv = models.IntegerField(u'网站点击访问量')

    def __unicode__(self):
        return self.access_time


# IP统计
class Access_ip(models.Model):
    ip = models.CharField(u'ip地址',max_length=30, primary_key=True)
    ip_attribution = models.CharField(u'ip归属地', max_length=10)


