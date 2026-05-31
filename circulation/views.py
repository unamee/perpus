from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import User
from books.models import Book, BookCopy
from circulation.models import BorrowPolicy, BorrowTransaction, Reservation
from schools.models import School


@login_required
def reservation_pickup(request):

    reservation_id = request.POST.get("reservation_id")

    reservation = Reservation.objects.get(id=reservation_id)

    available_copy = BookCopy.objects.filter(
        book=reservation.book, status="available"
    ).first()

    if not available_copy:

        return HttpResponse("No available copy.")

    BorrowTransaction.objects.create(
        school=reservation.school,
        borrower=reservation.user,
        book_copy=available_copy,
        status="borrowed",
    )

    reservation.status = "completed"

    reservation.save()

    return HttpResponse("Pickup completed.")


@login_required
def reservation_queue(request):

    reservations = Reservation.objects.select_related("user", "book").order_by(
        "reservation_date"
    )

    return render(
        request, "circulation/reservation_queue.html", {"reservations": reservations}
    )


@login_required
def reserve_submit(request):

    book_id = request.POST.get("book")

    user_id = request.POST.get("user")

    try:

        user = User.objects.get(id=user_id)

        book = Book.objects.get(id=book_id)

        reservation = Reservation.objects.create(
            school=user.school, user=user, book=book
        )

        return render(
            request,
            "circulation/partials/reserve_success.html",
            {"reservation": reservation},
        )

    except Exception as e:

        return HttpResponse(str(e))


@login_required
def reserve_page(request):

    context = {
        "books": Book.objects.all(),
        "users": User.objects.filter(role__in=["student", "teacher"]),
    }

    return render(request, "circulation/reserve.html", context)


@login_required
@role_required(["superadmin", "school_admin", "librarian"])
def borrow_page(request):

    borrowers = User.objects.filter(role__in=["student", "teacher"])

    return render(request, "circulation/borrow.html", {"borrowers": borrowers})


@login_required
def barcode_lookup(request):

    barcode = request.GET.get("barcode")

    book_copy = None

    if barcode:

        try:

            book_copy = BookCopy.objects.select_related("book", "shelf").get(
                barcode=barcode
            )

        except BookCopy.DoesNotExist:

            pass

    return render(
        request, "circulation/partials/book_lookup.html", {"book_copy": book_copy}
    )


@login_required
def borrow_submit(request):

    barcode = request.POST.get("barcode")

    borrower_id = request.POST.get("borrower")

    try:

        borrower = get_user_model().objects.get(id=borrower_id)

        book_copy = BookCopy.objects.get(barcode=barcode)

        school = borrower.school

        transaction = BorrowTransaction.objects.create(
            school=school,
            borrower=borrower,
            borrowed_by=request.user if request.user.is_authenticated else None,
            book_copy=book_copy,
            status="borrowed",
        )

        return render(
            request,
            "circulation/partials/borrow_success.html",
            {"transaction": transaction},
        )

    except Exception as e:

        return HttpResponse(f"""
            <div
                class='uk-alert-danger'
                uk-alert>

                {str(e)}

            </div>
            """)


@login_required
def due_date_preview(request):

    borrower_id = request.GET.get("borrower")

    context = {}

    if borrower_id:

        try:

            borrower = User.objects.get(id=borrower_id)

            policy = BorrowPolicy.objects.get(
                school=borrower.school, role=borrower.role, is_active=True
            )

            borrow_date = timezone.now().date()

            due_date = borrow_date + timezone.timedelta(days=policy.loan_days)

            context = {
                "borrower": borrower,
                "policy": policy,
                "borrow_date": borrow_date,
                "due_date": due_date,
            }

        except:

            pass

    return render(request, "circulation/partials/due_date_preview.html", context)


@login_required
def return_page(request):

    return render(request, "circulation/return.html")


@login_required
def return_lookup(request):

    barcode = request.GET.get("barcode")

    transaction = None

    if barcode:

        try:

            transaction = BorrowTransaction.objects.select_related(
                "borrower", "book_copy", "book_copy__book"
            ).get(book_copy__barcode=barcode, status="borrowed")

        except BorrowTransaction.DoesNotExist:

            pass

    return render(
        request, "circulation/partials/return_lookup.html", {"transaction": transaction}
    )


@login_required
def return_submit(request):

    transaction_id = request.POST.get("transaction_id")

    try:

        transaction = BorrowTransaction.objects.get(id=transaction_id)

        transaction.return_date = timezone.now().date()

        transaction.status = "returned"

        transaction.save()

        return render(
            request,
            "circulation/partials/return_success.html",
            {"transaction": transaction},
        )

    except Exception as e:

        return HttpResponse(f"""
            <div
                class='uk-alert-danger'
                uk-alert>

                {str(e)}

            </div>
            """)
