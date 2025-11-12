from django.shortcuts import render, redirect
from .forms import OrderForm

def create_order(request):
    initial_data = {}
    product_id = request.GET.get('product')
    if product_id:
        initial_data['product'] = product_id

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm(initial=initial_data)
    return render(request, 'orders/order_form.html', {'form': form})
