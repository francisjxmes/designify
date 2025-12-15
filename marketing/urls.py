from django.urls import path
from .views import newsletter_signup

urlpatterns = [
    path("signup/", newsletter_signup, name="newsletter_signup"),
]
