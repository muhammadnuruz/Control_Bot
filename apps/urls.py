from django.urls import path, include


urlpatterns = [
    path('messages/', include("apps.analyses.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
]
