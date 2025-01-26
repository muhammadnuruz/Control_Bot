from django.contrib import admin

from apps.bosses.models import Bosses


class BossesAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'created_at')
    ordering = ('created_at',)


admin.site.register(Bosses, BossesAdmin)
