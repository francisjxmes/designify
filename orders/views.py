from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DesignOrderForm
from .models import DesignOrder, DesignPackage
from .utils import calculate_quote


@login_required
def order_list(request):
    orders = DesignOrder.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_create(request):
    if request.method == "POST":
        form = DesignOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # server-side price (cannot be manipulated by user)
            order.quoted_price_eur = calculate_quote(
                base_price_eur=order.package.base_price_eur,
                design_type=order.design_type,
                size=order.size,
                brief=order.brief,
            )
            order.status = "draft"
            order.save()

            messages.success(request, "Order created. Review it and proceed to payment when ready.")
            return redirect("order_detail", order_id=order.id)
        messages.error(request, "Please fix the errors below.")
    else:
        form = DesignOrderForm()

    return render(request, "orders/order_form.html", {"form": form, "mode": "create"})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_edit(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)

    if order.status != "draft":
        messages.warning(request, "Only draft orders can be edited.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        form = DesignOrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)

            order.quoted_price_eur = calculate_quote(
                base_price_eur=order.package.base_price_eur,
                design_type=order.design_type,
                size=order.size,
                brief=order.brief,
            )
            order.save()
            messages.success(request, "Order updated.")
            return redirect("order_detail", order_id=order.id)
        messages.error(request, "Please fix the errors below.")
    else:
        form = DesignOrderForm(instance=order)

    return render(request, "orders/order_form.html", {"form": form, "mode": "edit"})


@login_required
def order_delete(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id, user=request.user)

    if order.status != "draft":
        messages.warning(request, "Only draft orders can be deleted.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted.")
        return redirect("order_list")

    return render(request, "orders/order_confirm_delete.html", {"order": order})
