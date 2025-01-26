from apps.groups.models import Groups
from apps.groups.serializers import GroupsSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class GroupsRetrieveView(generics.RetrieveAPIView):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'chat_id'
