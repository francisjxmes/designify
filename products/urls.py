from django.urls import path
from .views import home, delete_product, subscribe  

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('subscribe/', subscribe, name='subscribe'),  
]

