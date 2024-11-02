from django.urls import path

from apps.analyses.views import MessageCreateView, MessageUpdateView, MessageRetrieveView

urlpatterns = [
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<str:message_id>/update/', MessageUpdateView.as_view(), name='message-update'),
    path('messages/<str:message_id>/', MessageRetrieveView.as_view(), name='message-retrieve'),
]
