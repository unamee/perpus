from django.db import models
from django.utils import timezone


class BorrowTransaction(models.Model):

    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    )

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE
    )

    borrower = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    book_copy = models.ForeignKey(
        'books.BookCopy',
        on_delete=models.CASCADE
    )

    borrowed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='borrow_processed_by'
    )

    borrow_date = models.DateField(
        default=timezone.now
    )

    due_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='borrowed'
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.borrower} - {self.book_copy}'

class Fine(models.Model):

    transaction = models.OneToOneField(
        BorrowTransaction,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_paid = models.BooleanField(default=False)

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.amount)

class Reservation(models.Model):

    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE
    )

    reservation_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )
