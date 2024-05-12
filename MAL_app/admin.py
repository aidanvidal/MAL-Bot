from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'User Profile'
    fields = ('access_token', 'refresh_token')

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default User admin
admin.site.unregister(User)

# Register User admin with UserProfileInline
admin.site.register(User, CustomUserAdmin)
