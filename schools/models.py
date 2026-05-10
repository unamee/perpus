from django.db import models


# Create your models here.
class School(models.Model):
    LEVEL_CHOICES = (
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
    )

    name = models.CharField(max_length=255)

    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES
    )

    address = models.TextField(blank=True)

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(blank=True)

    logo = models.ImageField(
        upload_to='school_logos/',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
