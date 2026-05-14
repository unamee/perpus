from django.contrib import admin

from .models import AcademicYear, Classroom, Grade


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'school',
        'start_date',
        'end_date',
        'is_active'
    )

    list_filter = (
        'school',
        'is_active'
    )

    search_fields = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'school'
    )

    list_filter = ('school',)

    search_fields = ('name',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'grade',
        'school',
        'academic_year',
        'homeroom_teacher'
    )

    list_filter = (
        'school',
        'grade',
        'academic_year'
    )

    search_fields = ('name',)
