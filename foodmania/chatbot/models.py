from django.db import models

class Messages(models.Model):
    chat_id = models.CharField(max_length=255)
    message = models.TextField()
