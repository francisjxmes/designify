from django.urls import path
from . import views

urlpatterns = [
    path("checkout/<int:order_id>/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.payment_success, name="payment_success"),
    path("cancel/<int:order_id>/", views.payment_cancel, name="payment_cancel"),
]
