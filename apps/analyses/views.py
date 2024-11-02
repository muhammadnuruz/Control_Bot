from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.analyses.models import Messages
from apps.analyses.serializers import MessagesSerializer, MessagesCreateSerializer


# View to create a message
class MessageView(generics.ListAPIView):
    queryset = Messages.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessagesSerializer


class MessageCreateView(generics.CreateAPIView):
    queryset = Messages.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessagesSerializer


# View to update a message by message_id
class MessageUpdateView(generics.UpdateAPIView):
    queryset = Messages.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessagesCreateSerializer
    lookup_field = 'message_id'


# View to retrieve a message by message_id
class MessageRetrieveView(generics.RetrieveAPIView):
    queryset = Messages.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MessagesSerializer
    lookup_field = 'message_id'


class StatisticsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()

        # Umumiy savollar va javob berilmagan savollar
        total_questions = Messages.objects.count()
        total_unanswered = Messages.objects.filter(replied=False).count()

        # Oylik savollar va javob berilmagan savollar
        monthly_questions = Messages.objects.filter(created_at__month=now.month).count()
        monthly_unanswered = Messages.objects.filter(
            created_at__month=now.month, replied=False
        ).count()

        # Haftalik savollar va javob berilmagan savollar
        weekly_questions = Messages.objects.filter(
            created_at__gte=now - timezone.timedelta(days=7)
        ).count()
        weekly_unanswered = Messages.objects.filter(
            created_at__gte=now - timezone.timedelta(days=7), replied=False
        ).count()

        stats = {
            "total_questions": total_questions,
            "total_unanswered": total_unanswered,
            "monthly_questions": monthly_questions,
            "monthly_unanswered": monthly_unanswered,
            "weekly_questions": weekly_questions,
            "weekly_unanswered": weekly_unanswered,
        }
        return Response(stats)