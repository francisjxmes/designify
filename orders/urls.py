from django.urls import path
from . import views
from .views import (
    add_to_order,
    view_order,
    my_orders,
    stripe_checkout,
    checkout_success,
    checkout_cancel,
    stripe_webhook,
)

urlpatterns = [
    path('add/<int:product_id>/', add_to_order, name='add_to_order'),
    path('cart/', view_order, name='view_order'),
    path('my-orders/', my_orders, name='my_orders'),
    path('checkout/<int:order_id>/', stripe_checkout, name='stripe_checkout'),
    path('success/', checkout_success, name='checkout_success'),
    path('cancel/', checkout_cancel, name='checkout_cancel'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]


