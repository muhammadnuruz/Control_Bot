from rest_framework import serializers

from apps.analyses.models import Messages


class MessagesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ['created_at', 'updated_at']


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
