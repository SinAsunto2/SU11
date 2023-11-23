from django.contrib import admin
from .models import Challenge, CompletedChallenge, ChatMessage, Secrets, CompletedSecrets

# Register your models here.

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'keyword', 'challenge_hint')

class CompletedChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge')

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')

class SecretsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'keyword', 'points')

class CompletedSecretsAdmin(admin.ModelAdmin):
    list_display = ('user', 'secrets')

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(CompletedChallenge, CompletedChallengeAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Secrets, SecretsAdmin)
admin.site.register(CompletedSecrets, CompletedSecretsAdmin)