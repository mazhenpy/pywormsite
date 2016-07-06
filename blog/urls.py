from django.conf.urls import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                (r'^$','blog.views.blog'),
                (r'^to_mysql/$','blog.views.to_mysql'),
                (r'^to_summary/$','blog.views.to_summary'),
                (r'^test/$','blog.views.test'),
                )
