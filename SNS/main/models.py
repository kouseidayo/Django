from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Comment(models.Model):
    comment_text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(),verbose_name="ユーザー",on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment_text)
    
    
class Message(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(),verbose_name="ユーザー",on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(get_user_model(), related_name='liked_posts', blank=True)
    commented_by = models.ManyToManyField(Comment, related_name='comment', blank=True)

    def __str__(self):
        return str(self.msg_text)

    
