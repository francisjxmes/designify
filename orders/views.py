from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

@login_required
def create_order(request):
    initial_data = {}
    product_id = request.GET.get('product')
    if product_id:
        initial_data['product'] = product_id

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # assign logged-in user
            order.save()
            return redirect('home')
    else:
        form = OrderForm(initial=initial_data)

    return render(request, 'orders/order_form.html', {'form': form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})