from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

##from main.models import Follow


class CustomUser(AbstractUser):
 
  age = models.IntegerField(verbose_name="age",null=False,default=20)
  profile = models.TextField(verbose_name="profile",null=True)
##  follow = models.ManyToManyField(Follow,verbose_name='follow',blank=True)
  following = models.ManyToManyField('self',symmetrical=False, related_name='followers', related_query_name='follower')
