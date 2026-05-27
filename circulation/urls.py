from django.urls import path

from .views import (
    barcode_lookup,
    borrow_page,
    borrow_submit,
    due_date_preview,
    return_lookup,
    return_page,
    return_submit,     
)

urlpatterns = [
    path("borrow/", borrow_page, name="borrow_page"),
    path("barcode-lookup/", barcode_lookup, name="barcode_lookup"),
    path("borrow-submit/", borrow_submit, name="borrow_submit"),
    path("due-date-preview/", due_date_preview, name="due_date_preview"),
    path("return/", return_page, name="return_page"),
    path("return-lookup/", return_lookup, name="return_lookup"),
    path("return-submit/", return_submit, name="return_submit"),
]
