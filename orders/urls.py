from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_order, name='add_to_order'), 
    path('cart/', views.view_order, name='view_order'),                        
    path('my-orders/', views.my_orders, name='my_orders'),  
    path('checkout/<int:order_id>/', stripe_checkout, name='stripe_checkout'),
    path('success/', TemplateView.as_view(template_name='orders/success.html'), name='checkout_success'),
    path('cancel/', TemplateView.as_view(template_name='orders/cancel.html'), name='checkout_cancel'),
                   
]

