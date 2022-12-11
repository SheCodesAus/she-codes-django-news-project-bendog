from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
class Example(models.Model):
    name = models.CharField(max_length=18)
    thing = models.BooleanField()