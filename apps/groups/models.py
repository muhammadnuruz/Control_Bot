from django.db import models

from apps.bosses.models import Bosses


class Groups(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    companies = models.ManyToManyField(Bosses, related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return f"{self.companies}"
