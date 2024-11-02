from rest_framework import generics

from apps.analyses.models import Messages
from apps.analyses.serializers import MessagesSerializer, MessagesCreateSerializer


# View to create a message
class MessageCreateView(generics.CreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer


# View to update a message by message_id
class MessageUpdateView(generics.UpdateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesCreateSerializer
    lookup_field = 'message_id'


# View to retrieve a message by message_id
class MessageRetrieveView(generics.RetrieveAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    lookup_field = 'message_id'
