from django.db import models


class Bosses(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Boss"
        verbose_name_plural = "Bosses"

    def __str__(self):
        return f"{self.name}"
