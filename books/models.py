from django.db import models


class Category(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publisher(models.Model):

    name = models.CharField(max_length=255)

    city = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.name


class Author(models.Model):

    name = models.CharField(max_length=255)

    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Shelf(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=50)

    location = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Book(models.Model):

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True
    )

    authors = models.ManyToManyField(Author)

    title = models.CharField(max_length=255)

    isbn = models.CharField(
        max_length=30,
        blank=True
    )

    publication_year = models.IntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    cover = models.ImageField(
        upload_to='book_covers/',
        null=True,
        blank=True
    )

    language = models.CharField(
        max_length=50,
        default='Indonesia'
    )

    pages = models.IntegerField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookCopy(models.Model):

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost'),
        ('maintenance', 'Maintenance'),
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.SET_NULL,
        null=True
    )

    barcode = models.CharField(
        max_length=100,
        unique=True
    )

    acquisition_date = models.DateField(
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.barcode
