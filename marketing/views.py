from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import NewsletterSignupForm

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You’re signed up — cheers! 🎉")
        else:
            messages.error(request, "That email doesn’t look right, try again.")
    return redirect("home")
