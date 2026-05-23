from django.urls import path

from .views import barcode_lookup, borrow_page

urlpatterns = [
    path("borrow/", borrow_page, name="borrow_page"),
    path("barcode-lookup/", barcode_lookup, name="barcode_lookup"),
]
