from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BorrowPolicy(models.Model):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("librarian", "Librarian"),
    )

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    max_books = models.PositiveIntegerField(default=3)

    loan_days = models.PositiveIntegerField(default=7)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "role")

    def __str__(self):

        return f"{self.school} - {self.role}"


class BorrowTransaction(models.Model):

    STATUS_CHOICES = (
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("late", "Late"),
    )

    school = models.ForeignKey(
        "schools.School", on_delete=models.CASCADE, related_name="borrow_transactions"
    )

    borrower = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="borrow_transactions"
    )

    book_copy = models.ForeignKey(
        "books.BookCopy", on_delete=models.CASCADE, related_name="borrow_transactions"
    )

    borrowed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_borrow_transactions",
    )

    borrow_date = models.DateField(default=timezone.now)

    due_date = models.DateField(null=True, blank=True)

    return_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-borrow_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["borrow_date"]),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        # Auto due date
        if not self.due_date and self.status == 'borrowed':
            policy = BorrowPolicy.objects.get(
                school=self.school,
                role=self.borrower.role,
                is_active=True
            )
            self.due_date = (
                self.borrow_date +
                timezone.timedelta(days=policy.loan_days)
            )

        # save transaction dulu
        super().save(*args, **kwargs)
        # update inventory setelah transaction sukses
        if self.status == "borrowed":
            if self.book_copy.status != "borrowed":
                self.book_copy.status = "borrowed"
                self.book_copy.save()

        elif self.status == "returned":
            if self.book_copy.status != "available":
                self.book_copy.status = "available"
                self.book_copy.save()
                next_reservation = Reservation.objects.filter(
                    book=self.book_copy.book,
                    status='waiting'
                ).order_by(
                    'reservation_date'
                ).first()
                if next_reservation:
                    next_reservation.status='ready'
                    next_reservation.save()

            # Fine calculation
            if self.return_date and self.return_date > self.due_date:
                late_days = (self.return_date - self.due_date).days

                fine_amount = Decimal(
                    late_days * 1000
                )  # Contoh perhitungan denda: 1000 per hari keterlambatan
                Fine.objects.get_or_create(
                    transaction=self, defaults={"amount": fine_amount}
                )

    def clean(self):
        if self.status == "borrowed":
            if not self.pk:
                fresh_book_copy = self.book_copy.__class__.objects.get(
                    pk=self.book_copy.pk
                )
                if fresh_book_copy.status != "available":
                    raise ValidationError("Book is not available for borrowing.")
                # cek borrow policy
                policy = BorrowPolicy.objects.get(
                    school=self.school, role=self.borrower.role, is_active=True
                )
                active_loans = BorrowTransaction.objects.filter(
                    borrower=self.borrower, status="borrowed"
                ).count()

                if active_loans >= policy.max_books:
                    raise ValidationError(f"Borrow limit exceeded ({policy.max_books})")

    @property
    def is_overdue(self):
        if self.status == "borrowed":
            return timezone.now().date() > self.due_date
        return False

    @property
    def overdue_days(self):
        if self.is_overdue:
            return (timezone.now().date() - self.due_date).days
        return 0

    def __str__(self):
        return f"{self.borrower} - {self.book_copy}"


class Fine(models.Model):

    transaction = models.OneToOneField(
        BorrowTransaction, on_delete=models.CASCADE, related_name="fine"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    paid_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.amount)


class Reservation(models.Model):

    STATUS_CHOICES = (
        ("waiting", "Waiting"),
        ('ready','Ready'),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="reservations"
    )

    reservation_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reservation_date"]

    def __str__(self):
        return f"{self.user} - {self.book}"
