from django.db.models import Count
from django.utils import timezone

from accounts.models import User
from books.models import Book, BookCopy
from circulation.models import BorrowTransaction, Fine


def active_borrow_report():

    return BorrowTransaction.objects.filter(status="borrowed").select_related(
        "borrower", "book_copy", "book_copy__book"
    )


def overdue_report():

    today = timezone.now().date()

    return BorrowTransaction.objects.filter(status="borrowed", due_date__lt=today)


def unpaid_fine_report():

    return Fine.objects.filter(is_paid=False).select_related(
        "transaction", "transaction__borrower"
    )


def most_borrowed_books():

    return Book.objects.annotate(
        borrow_count=Count("copies__borrow_transactions")
    ).order_by("-borrow_count")


def top_readers():

    return User.objects.annotate(total_borrow=Count("borrow_transactions")).order_by(
        "-total_borrow"
    )


def inventory_summary():

    return BookCopy.objects.values("status").annotate(total=Count("id"))
