from django.urls import path

from apps.analyses.views import MessageCreateView, MessageRetrieveView, MessageView, StatisticsAPIView, MessageDeleteView

urlpatterns = [
    path('messages/', MessageView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<str:chat_id>/', MessageRetrieveView.as_view(), name='message-retrieve'),
    path('messages/statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('messages/<chat_id:str>/delete/', MessageDeleteView.as_view(), name='message-delete'),
]
