from rest_framework import serializers
from apps.groups.models import Groups
from apps.bosses.models import Bosses


class GroupsSerializer(serializers.ModelSerializer):
    owners = serializers.SerializerMethodField()

    class Meta:
        model = Groups
        fields = '__all__'

    def get_owners(self, obj):
        return obj.owners.values_list('chat_id', flat=True)
