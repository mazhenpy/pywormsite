from django.conf.urls import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                (r'^$','blog.views.blog'),
                (r'^to_mysql/$','blog.views.to_mysql'),
                (r'^test/$','blog.views.test'),
                )
