from rest_framework import serializers

from apps.bosses.models import Bosses


class BossesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bosses
        fields = '__all__'
