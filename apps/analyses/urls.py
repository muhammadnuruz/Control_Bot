from django.urls import path

from apps.analyses.views import MessageCreateView, MessageUpdateView, MessageRetrieveView, MessageView, \
    StatisticsAPIView, UserLastMessageAPIView

urlpatterns = [
    path('messages/', MessageView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<str:message_id>/update/', MessageUpdateView.as_view(), name='message-update'),
    path('messages/<str:message_id>/', MessageRetrieveView.as_view(), name='message-retrieve'),
    path('messages/statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('messages/user-last-message/<str:user_id>/', UserLastMessageAPIView.as_view(), name='user-last-message'),
]
