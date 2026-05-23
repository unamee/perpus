from django.contrib import admin

from .models import BorrowPolicy, BorrowTransaction, Fine, Reservation


@admin.register(BorrowPolicy)
class BorrowPolicyAdmin(admin.ModelAdmin):

    list_display = (
        'school',
        'role',
        'max_books',
        'loan_days',
        'is_active'
    )

    list_filter = (
        'school',
        'role'
    )

@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "borrower",
        "book_copy",
        "borrow_date",
        "due_date",
        "return_date",
        "status",
        "is_overdue",
        "overdue_days",
        "is_overdue_display",
    )

    search_fields = (
        "borrower__username",
        "borrower__first_name",
        "book_copy__barcode",
        "book_copy__inventory_code",
        "book_copy__book__title",
    )

    readonly_fields = (
        'due_date',
    )

    list_filter = ("status", "borrow_date", "due_date", "school")

    autocomplete_fields = ("borrower", "book_copy", "borrowed_by")

    date_hierarchy = "borrow_date"

    ordering = ("-borrow_date",)

    list_per_page = 25

    def is_overdue_display(self, obj):
        return obj.is_overdue
    is_overdue_display.boolean = True
    is_overdue_display.short_description = 'Overdue'

    def overdue_days_display(self, obj):
        return obj.overdue_days
    overdue_days_display.short_description = 'Late Days'


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
