from django.urls import path, include

urlpatterns = [
    path('messages/', include("apps.analyses.urls")),
    path('groups/', include("apps.groups.urls")),
]
