from django.contrib import admin

from apps.telegram_users.models import TelegramUsers


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name','chat_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('chat_id', 'username', 'full_name', 'phone_number')
    ordering = ('chat_id', 'created_at')


admin.site.register(TelegramUsers, TelegramUsersAdmin)
