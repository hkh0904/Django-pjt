from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_img = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        super().save(*args, **kwargs)