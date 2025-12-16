from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import RegisterForm

def home(request):
    return render(request, "home.html")


def anonymous_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return _wrapped


@anonymous_required
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created — welcome to Designify!")
            return redirect("home")
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        form.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        return form

    def get_success_url(self):
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Sitemap: " + request.build_absolute_uri("/sitemap.xml"),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")