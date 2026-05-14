from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'school',
        'is_active',
        'is_staff',
        'created_at'
    )

    list_filter = (
        'role',
        'school',
        'is_active',
        'is_staff'
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )

    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (
            'Library Information',
            {
                'fields': (
                    'role',
                    'school',
                    'phone_number',
                    'avatar',
                    'is_active_member'
                )
            }
        ),
    )
