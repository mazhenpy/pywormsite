from django.contrib import admin
from blog.models import Blog, Replay, IP_access


class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_id',)


class ReplayAdmin(admin.ModelAdmin):
    list_display = ('blog', 'replay_time')

class IP_accessAdmin(admin.ModelAdmin):
    list_display = ('ip', )


admin.site.register(Blog, BlogAdmin)
admin.site.register(Replay, ReplayAdmin)
admin.site.register(IP_access, IP_accessAdmin)