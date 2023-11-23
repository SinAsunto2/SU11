from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserActivity

from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ('username', 'full_name', 'email', 'is_staff', 'is_superuser', 'score', 'is_vip', 'is_online', 'is_verified')
    # Agrega los campos adicionales aquí, incluyendo password
    fieldsets = (
        ('Personal info', {
            'fields': ('username', 'score', 'full_name', 'email', 'profile_picture', 'description', 'is_vip', 'is_online', 'is_verified'),
        }),
        ('Password', {
            'fields': ('password',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    list_filter = ('user',)
    search_fields = ('user__username', 'activity_type')
    ordering = ('-timestamp',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserActivity, UserActivityAdmin)

