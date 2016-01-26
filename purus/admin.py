from django.contrib import admin
from purus.models import Access_amount_mon, Access_amount_day, Access_ip


class Access_amount_monAdmin(admin.ModelAdmin):
    list_display = ('access_time',)


class Access_amount_dayAdmin(admin.ModelAdmin):
    list_display = ('access_time',)

class Access_ipAdmin(admin.ModelAdmin):
    list_display = ('ip', )


admin.site.register(Access_amount_mon, Access_amount_monAdmin)
admin.site.register(Access_amount_day, Access_amount_dayAdmin)
admin.site.register(Access_ip, Access_ipAdmin)
