from django.contrib import admin

from blog.models import Blog, Replay


class BlogAdmin(admin.ModelAdmin):

    list_display = ('blog_id',)

    # class Media:
    #     js = (
    #         "/static/kindeditor-4.1.10/kindeditor-min.js",
    #         "/static/kindeditor-4.1.10/lang/zh_CN.js",
    #         "/static/kindeditor-4.1.10/config.js",
    #     )


class ReplayAdmin(admin.ModelAdmin):
    list_display = ('blog', 'replay_time')


# admin.site.register(Blog, BlogAdmin)
# admin.site.register(Replay, ReplayAdmin)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Replay, ReplayAdmin)
