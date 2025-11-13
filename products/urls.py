from django.urls import path
from .views import home, delete_product, subscribe 
from . import views 

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('subscribe/', subscribe, name='subscribe'),  
]

