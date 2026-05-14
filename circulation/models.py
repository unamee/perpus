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
        on_delete=models.CASCADE,
        related_name='borrow_transactions'
    )

    borrower = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='borrow_transactions'
    )

    book_copy = models.ForeignKey(
        'books.BookCopy',
        on_delete=models.CASCADE
    )

    borrowed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_borrow_transactions'
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

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-borrow_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['borrow_date']),
        ]

    def __str__(self):
        return f'{self.borrower} - {self.book_copy}'

class Fine(models.Model):

    transaction = models.OneToOneField(
        BorrowTransaction,
        on_delete=models.CASCADE,
        related_name='fine'
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

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

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
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    reservation_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reservation_date']

    def __str__(self):
        return f'{self.user} - {self.book}'
