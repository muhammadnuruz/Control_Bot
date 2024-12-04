from django.contrib import admin

from apps.analyses.models import Messages


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'chat_id', 'message_id', 'created_at')
    ordering = ('created_at',)


admin.site.register(Messages, MessagesAdmin)
