from django.shortcuts import render

from books.models import BookCopy


# Create your views here.
def borrow_page(request):

    return render(request, "circulation/borrow.html")


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
