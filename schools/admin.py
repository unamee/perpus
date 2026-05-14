from django.contrib import admin

from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'level',
        'phone',
        'email',
        'is_active'
    )

    search_fields = (
        'name',
        'email'
    )

    list_filter = (
        'level',
        'is_active'
    )

    ordering = ('name',)
