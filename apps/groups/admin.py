from django.contrib import admin
from apps.groups.models import Groups


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'get_companies', 'created_at')  # get_companies funksiyasidan foydalanamiz
    list_filter = ('created_at',)  # Filtrlash uchun maydon
    search_fields = ('chat_id',)  # Qidiruv maydoni
    ordering = ('-created_at',)  # Oxirgi qo‘shilganlarni birinchi ko‘rsatish
    date_hierarchy = 'created_at'  # Vaqt bo‘yicha tez navigatsiya qilish

    def get_companies(self, obj):
        return ", ".join([owner.name for owner in obj.companies.all()])

    get_companies.short_description = 'Companies'  # Admin paneldagi ustun nomi
