from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keyword = models.CharField(max_length=100, null=False, default='RETO')
    challenge_hint = models.TextField(null=True, blank=True)

class CompletedChallenge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username if self.sender else "Klin"} - {self.timestamp}'
    


class Secrets(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keyword = models.CharField(max_length=100, null=False, default='S')
    points = models.IntegerField(default=1000)

class CompletedSecrets(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    secrets = models.ForeignKey(Secrets, on_delete=models.CASCADE)