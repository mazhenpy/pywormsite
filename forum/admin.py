from django.contrib import admin
from forum.models import Post,Replay

class PostAdmin(admin.ModelAdmin):
        list_display = ('title','post_time')

class ReplayAdmin(admin.ModelAdmin):
        list_display = ('post','replay_time')

admin.site.register(Post,PostAdmin)
admin.site.register(Replay,ReplayAdmin)
