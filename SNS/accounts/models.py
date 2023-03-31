from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
 
  age = models.IntegerField(
    verbose_name="age",
    null=False,
    default=20,
  )
