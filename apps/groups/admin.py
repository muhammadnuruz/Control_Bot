from django.contrib import admin
from apps.groups.models import Groups


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'get_owners', 'created_at')  # get_owners funksiyasidan foydalanamiz
    list_filter = ('created_at',)  # Filtrlash uchun maydon
    search_fields = ('chat_id',)  # Qidiruv maydoni
    ordering = ('-created_at',)  # Oxirgi qo‘shilganlarni birinchi ko‘rsatish
    date_hierarchy = 'created_at'  # Vaqt bo‘yicha tez navigatsiya qilish

    def get_owners(self, obj):
        return ", ".join([owner.name for owner in obj.owners.all()])

    get_owners.short_description = 'Owners'  # Admin paneldagi ustun nomi
