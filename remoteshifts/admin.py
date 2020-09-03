from django.contrib import admin

from .models import LdapUser, FixedRemoteShift, ScheduledRemoteShift

class LdapUserAdmin(admin.ModelAdmin):
    list_display = ('supann_alias_login', 'given_name', 'sn', 'mail', 'uid')
    list_filter = ['given_name']

admin.site.register(LdapUser, LdapUserAdmin)
admin.site.register(FixedRemoteShift)
admin.site.register(ScheduledRemoteShift)
