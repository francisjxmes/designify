from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product

@login_required
def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, completed=False)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity
        order_item.save()
        return redirect('view_order')  # redirect to cart page

    return render(request, 'orders/add_to_order.html', {'product': product})

@login_required
def view_order(request):
    order = Order.objects.filter(user=request.user, completed=False).first()
    items = order.items.all() if order else []
    total = order.total_price() if order else 0
    return render(request, 'orders/view_order.html', {'order': order, 'items': items, 'total': total})
