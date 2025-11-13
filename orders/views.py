import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('client_reference_id')
        try:
            order = Order.objects.get(id=order_id)
            order.completed = True
            order.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)

@login_required
def stripe_checkout(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),  # cents
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/orders/success/'),
        cancel_url=request.build_absolute_uri('/orders/cancel/'),
        client_reference_id=str(order.id),
    )
    return redirect(session.url, code=303)

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
            order.user = request.user  
            order.save()
           
            form.save_m2m()
            return redirect('home')  
    else:
        form = OrderForm(initial=initial_data)

    return render(request, 'orders/order_form.html', {'form': form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'orders/my_orders.html', {'orders': orders})

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

@login_required
def checkout_success(request):
    return render(request, 'orders/checkout_success.html')

@login_required
def checkout_cancel(request):
    return render(request, 'orders/checkout_cancel.html')

