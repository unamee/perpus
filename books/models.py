import uuid

from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    school = models.ForeignKey(
        "schools.School", on_delete=models.CASCADE, related_name="categories"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=120, blank=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["school", "name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(models.Model):

    name = models.CharField(max_length=255)

    city = models.CharField(max_length=100, blank=True)

    email = models.EmailField(blank=True)

    website = models.URLField(blank=True)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):

    name = models.CharField(max_length=255)

    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to="authors/", null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Shelf(models.Model):

    school = models.ForeignKey(
        "schools.School", on_delete=models.CASCADE, related_name="shelves"
    )

    code = models.CharField(max_length=50)

    location = models.CharField(max_length=255)
    floor = models.CharField(max_length=50, blank=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]
        unique_together = ["school", "code"]

    def __str__(self):
        return self.code


class Book(models.Model):

    LANGUAGE_CHOICES = (
        ("id", "Indonesia"),
        ("en", "English"),
        ("cn", "Chinese"),
        ("jp", "Japanese"),
    )

    school = models.ForeignKey(
        "schools.School", on_delete=models.CASCADE, related_name="books"
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="books"
    )

    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, related_name="books"
    )

    authors = models.ManyToManyField(Author)

    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=300, blank=True)

    isbn = models.CharField(max_length=30, blank=True)

    edition = models.CharField(max_length=50, blank=True)

    publication_year = models.IntegerField(null=True, blank=True)

    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="id")

    description = models.TextField(blank=True)

    synopsis = models.TextField(blank=True)

    cover = models.ImageField(upload_to="books/covers/", null=True, blank=True)

    pages = models.PositiveIntegerField(null=True, blank=True)

    thumbnail = models.ImageField(upload_to="books/thumbnails/", null=True, blank=True)

    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_books",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookCopy(models.Model):

    STATUS_CHOICES = (
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("reserved", "Reserved"),
        ("lost", "Lost"),
        ("maintenance", "Maintenance"),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")

    shelf = models.ForeignKey(
        Shelf, on_delete=models.SET_NULL, null=True, related_name="book_copies"
    )

    barcode = models.CharField(max_length=100, unique=True)

    acquisition_date = models.DateField(null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    condition = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )

    notes = models.TextField(blank=True)

    qr_code = models.ImageField(upload_to="books/qrcodes/", null=True, blank=True)

    inventory_code = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["barcode"]
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["inventory_code"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):

        if not self.barcode:
            self.barcode = str(uuid.uuid4()).split("-")[0]

        if not self.inventory_code:
            self.inventory_code = f"INV-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.barcode
