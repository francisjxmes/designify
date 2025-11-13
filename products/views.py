from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Product, Subscriber
from .forms import SubscriberForm

def home(request):
    products = Product.objects.all()
    newsletter_form = SubscriberForm()
    return render(request, 'home.html', {
        'products': products,
        'newsletter_form': newsletter_form
    })

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # prevent duplicate subscription
            if Subscriber.objects.filter(email=email).exists():
                messages.info(request, "You're already subscribed to the newsletter.")
            else:
                form.save()
                messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect('home')

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('home')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})