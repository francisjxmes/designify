from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import SubscriberForm

def home(request):
    products = Product.objects.all()
    newsletter_form = SubscriberForm()  # Add the newsletter form
    return render(request, 'home.html', {
        'products': products,
        'newsletter_form': newsletter_form
    })

# Only staff users can delete products
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')

# Newsletter subscription handling
def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect after successful submission
    return redirect('home')
