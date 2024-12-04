from django.db import models


class Messages(models.Model):
    user_id = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100, unique=True)
    message_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Habar "
        verbose_name_plural = "Habarlar "

    def __str__(self):
        return f"{self.user_id}"
