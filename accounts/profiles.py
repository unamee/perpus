from django.db import models


class StudentProfile(models.Model):

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
    )

    nis = models.CharField(
        max_length=50,
        unique=True
    )

    classroom = models.ForeignKey(
        'academics.Classroom',
        on_delete=models.SET_NULL,
        null=True
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    address = models.TextField(blank=True)

    parent_name = models.CharField(
        max_length=255,
        blank=True
    )

    parent_phone = models.CharField(
        max_length=30,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()


class TeacherProfile(models.Model):

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
    )

    nip = models.CharField(
        max_length=50,
        unique=True
    )

    position = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.get_full_name()
