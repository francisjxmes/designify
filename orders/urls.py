from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_order, name='add_to_order'), 
    path('cart/', views.view_order, name='view_order'),                        
    path('my-orders/', views.my_orders, name='my_orders'),                     
]

