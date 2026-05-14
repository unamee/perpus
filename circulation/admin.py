from django.contrib import admin

from .models import BorrowTransaction, Fine, Reservation


@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "borrower",
        "book_copy",
        "borrow_date",
        "due_date",
        "return_date",
        "status",
    )

    search_fields = (
        "borrower__username",
        "borrower__first_name",
        "book_copy__barcode",
        "book_copy__inventory_code",
        "book_copy__book__title",
    )

    list_filter = ("status", "borrow_date", "due_date", "school")

    autocomplete_fields = ("borrower", "book_copy", "borrowed_by")

    date_hierarchy = "borrow_date"

    ordering = ("-borrow_date",)

    list_per_page = 25


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):

    list_display = ("transaction", "amount", "is_paid", "paid_at")

    search_fields = ("transaction__borrower__username",)

    list_filter = ("is_paid",)

    ordering = ("-id",)

    list_per_page = 25


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ("user", "book", "reservation_date", "status")

    search_fields = ("user__username", "book__title")

    list_filter = ("status",)

    ordering = ("-reservation_date",)

    list_per_page = 25
