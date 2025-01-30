from rest_framework import serializers
from apps.groups.models import Groups
from apps.bosses.models import Bosses


class GroupsSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField()

    class Meta:
        model = Groups
        fields = '__all__'

    def get_companies(self, obj):
        return obj.companies.values_list('chat_id', flat=True)
