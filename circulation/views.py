from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.models import User
from books.models import BookCopy
from circulation.models import BorrowPolicy, BorrowTransaction
from schools.models import School


# Create your views here.
def borrow_page(request):

    borrowers = User.objects.filter(role__in=["student", "teacher"])

    return render(request, "circulation/borrow.html", {"borrowers": borrowers})

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

def borrow_submit(request):

    barcode = request.POST.get('barcode')

    borrower_id = request.POST.get('borrower')

    try:

        borrower = get_user_model().objects.get(
            id=borrower_id
        )

        book_copy = BookCopy.objects.get(
            barcode=barcode
        )

        school = borrower.school

        transaction = BorrowTransaction.objects.create(
            school=school,
            borrower=borrower,
            borrowed_by=request.user
                if request.user.is_authenticated
                else None,
            book_copy=book_copy,
            status='borrowed'
        )

        return render(
            request,
            'circulation/partials/borrow_success.html',
            {
                'transaction': transaction
            }
        )

    except Exception as e:

        return HttpResponse(

            f"""
            <div
                class='uk-alert-danger'
                uk-alert>

                {str(e)}

            </div>
            """
        )

def due_date_preview(request):

    borrower_id = request.GET.get(
        'borrower'
    )

    context = {}

    if borrower_id:

        try:

            borrower = User.objects.get(
                id=borrower_id
            )

            policy = BorrowPolicy.objects.get(
                school=borrower.school,
                role=borrower.role,
                is_active=True
            )

            borrow_date = timezone.now().date()

            due_date = (
                borrow_date +
                timezone.timedelta(
                    days=policy.loan_days
                )
            )

            context = {

                'borrower': borrower,

                'policy': policy,

                'borrow_date': borrow_date,

                'due_date': due_date

            }

        except:

            pass

    return render(
        request,
        'circulation/partials/due_date_preview.html',
        context
    )

def return_page(request):

    return render(
        request,
        'circulation/return.html'
    )

def return_lookup(request):

    barcode = request.GET.get(
        'barcode'
    )

    transaction = None

    if barcode:

        try:

            transaction = BorrowTransaction.objects.select_related(
                'borrower',
                'book_copy',
                'book_copy__book'
            ).get(
                book_copy__barcode=barcode,
                status='borrowed'
            )

        except BorrowTransaction.DoesNotExist:

            pass

    return render(
        request,
        'circulation/partials/return_lookup.html',
        {
            'transaction': transaction
        }
    )


def return_submit(request):

    transaction_id = request.POST.get(
        'transaction_id'
    )

    try:

        transaction = BorrowTransaction.objects.get(
            id=transaction_id
        )

        transaction.return_date = (
            timezone.now().date()
        )

        transaction.status = 'returned'

        transaction.save()

        return render(
            request,
            'circulation/partials/return_success.html',
            {
                'transaction': transaction
            }
        )

    except Exception as e:

        return HttpResponse(

            f"""
            <div
                class='uk-alert-danger'
                uk-alert>

                {str(e)}

            </div>
            """
        )
