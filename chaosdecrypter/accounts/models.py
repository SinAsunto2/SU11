from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=50)
    is_vip = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    description = models.TextField(blank=True, max_length=255)

    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
# Ruta donde se encuentra la imagen por defecto
DEFAULT_PROFILE_PICTURE = 'profile_pics/blank_profile.png'

@receiver(pre_save, sender=CustomUser)
def set_default_profile_picture(sender, instance, **kwargs):
    if not instance.profile_picture:
        instance.profile_picture = DEFAULT_PROFILE_PICTURE


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)