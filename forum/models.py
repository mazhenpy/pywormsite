# coding:utf-8
from django.db import models

#定义帖子数据
class Post(models.Model):
    title = models.CharField(u'标题',max_length=100, blank=False)
    content = models.TextField(u'内容')
    read_num = models.IntegerField(u'阅读量', default=0)
    post_time = models.DateTimeField(u'发表时间')
    post_user = models.CharField(u'发表人',max_length=30)

    def __unicode__(self):
        return self.title


class Replay(models.Model):
    content = models.TextField(u'回复内容')
    post = models.ForeignKey(Post)
    replay_time = models.DateTimeField(u'回复时间')
    replay_user = models.CharField(u'回复者',max_length=30)

    def __unicode__(self):
        return self.replay_time


#定义小说数据
class Post14(models.Model):
    parent = models.ForeignKey('self', related_name='categories', null=True, blank=True)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField()
    read_num = models.IntegerField(u'阅读量', default=0)
    post_time = models.DateTimeField(u'发表时间')
    post_user = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title


class Replay14(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post14)
    replay_time = models.DateTimeField(u'回复时间')
    replay_user = models.CharField(max_length=30)

    def __unicode__(self):
        return self.replay_time


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog_photos')

    class Meta:
        ordering = ["title"]