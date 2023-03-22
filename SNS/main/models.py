from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

    
class Message(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_text = models.TextField()
    good = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(),verbose_name="ユーザー",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.msg_text)

    
