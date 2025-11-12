from django.urls import path
from .views import create_order, my_orders

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('my-orders/', my_orders, name='my_orders'),
]


