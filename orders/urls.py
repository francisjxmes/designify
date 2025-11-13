from django.urls import path
from . import views
from .views import stripe_webhook

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_order, name='add_to_order'), 
    path('cart/', views.view_order, name='view_order'),                        
    path('my-orders/', views.my_orders, name='my_orders'),  
    path('checkout/<int:order_id>/', stripe_checkout, name='stripe_checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),               
]

