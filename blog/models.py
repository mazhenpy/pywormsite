# coding:utf-8
from django.db import models


#博客
class Blog(models.Model):
    blog_id = models.IntegerField(u'博客ID', primary_key=True)
    title = models.CharField(u'标题',max_length=100)
    categorie = models.CharField(u'分类',max_length=10)
    content = models.TextField(u'内容')
    summary = models.CharField(u'摘要',max_length=200)
    PV_num = models.IntegerField(u'PV访问量', default=0)
    IP_num = models.IntegerField(u'IP访问量', default=0)
    post_time = models.DateTimeField(u'发表时间')

    def __unicode__(self):
        return self.blog_id


#博客的回复
class Replay(models.Model):
    blog = models.ForeignKey(Blog)
    parent_id = models.IntegerField(u'父ID',default=0)
    content = models.TextField(u'回复内容')
    replay_id = models.IntegerField(u'回复ID')
    replay_time = models.DateTimeField(u'回复时间')
    replay_user = models.CharField(u'回复者',max_length=30)

    def __unicode__(self):
        return self.replay_time


#浏览博客的IP
class IP_access(models.Model):
    ip = models.CharField(u'ip地址',max_length=30, primary_key=True)
    blogs = models.ManyToManyField(Blog)



