from django.db import models


class Ebook(models.Model):

    ACCESS_CHOICES = (
        ('public', 'Public'),
        ('member', 'Member'),
    )

    book = models.OneToOneField(
        'books.Book',
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='ebooks/'
    )

    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_CHOICES,
        default='member'
    )

    total_download = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
