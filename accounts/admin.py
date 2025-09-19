from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('username', 'first_name', 'email', 'profile_picture')
        }),
        ('Mot de Passe', {
            'fields': ('password',)  
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')
        }),
        ('Dates Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    

admin.site.register(User, UserAdmin)