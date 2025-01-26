from django.urls import path

from apps.groups.views import GroupsRetrieveView

urlpatterns = [
    path('<str:chat_id>/', GroupsRetrieveView.as_view(), name='groups-retrieve'),
]
