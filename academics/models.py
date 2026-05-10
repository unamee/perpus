from django.db import models


class AcademicYear(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='academic_years'
    )

    name = models.CharField(max_length=50)

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        unique_together = ['school', 'name']

    def __str__(self):
        return f'{self.school} - {self.name}'


class Grade(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='grades'
    )

    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ['school', 'name']

    def __str__(self):
        return f'{self.school} - {self.name}'


class Classroom(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    name = models.CharField(max_length=50)

    homeroom_teacher = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['grade', 'name']
        unique_together = [
            'school',
            'academic_year',
            'grade',
            'name'
        ]

    def __str__(self):
        return f'{self.grade} - {self.name}'
