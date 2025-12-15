import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import DesignOrder

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)

    if order.status != "draft":
        messages.warning(request, "Only draft orders can be paid for.")
        return redirect("order_detail", order_id=order.id)

    
    order.status = "awaiting_payment"
    order.save()

    success_url = request.build_absolute_uri(reverse("payment_success", args=[order.id]))
    cancel_url = request.build_absolute_uri(reverse("payment_cancel", args=[order.id]))


    amount_cents = int(order.quoted_price_eur * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": f"Designify — {order.package.name}",
                        "description": f"Order #{order.id}: {order.design_type}",
                    },
                    "unit_amount": amount_cents,
                },
                "quantity": 1,
            }
        ],
        metadata={"order_id": str(order.id), "user_id": str(request.user.id)},
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )

    return redirect(session.url, code=303)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)

    order.status = "paid"
    order.save()

    messages.success(request, "Payment successful ✅ Your order is now confirmed.")
    return render(request, "payments/success.html", {"order": order})


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)

    messages.error(request, "Payment cancelled. Your order is still saved — you can try again anytime.")
    return render(request, "payments/cancel.html", {"order": order})
