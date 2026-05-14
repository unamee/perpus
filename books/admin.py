from django.contrib import admin

from .models import (
    Author,
    Book,
    BookCopy,
    Category,
    Publisher,
    Shelf,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "school", "is_active", "created_at")

    search_fields = ("name",)

    list_filter = ("school", "is_active")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):

    list_display = ("name", "city", "email")

    search_fields = ("name", "city")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'birth_date'
    )

    search_fields = ('name',)

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'location',
        'school',
        'floor',
        'is_active'
    )

    search_fields = (
        'code',
        'location'
    )

    list_filter = (
        'school',
        'is_active'
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'isbn',
        'category',
        'publisher',
        'publication_year',
        'language',
        'is_active'
    )

    search_fields = (
        'title',
        'isbn'
    )

    list_filter = (
        'school',
        'category',
        'publisher',
        'language',
        'is_active'
    )

    filter_horizontal = ('authors',)

    list_per_page = 25

    ordering = ('title',)

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):

    list_display = (
        'barcode',
        'inventory_code',
        'book',
        'shelf',
        'status'
    )

    search_fields = (
        'barcode',
        'inventory_code',
        'book__title'
    )

    list_filter = (
        'status',
        'shelf'
    )

    autocomplete_fields = (
        'book',
    )

    list_per_page = 25
