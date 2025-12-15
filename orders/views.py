from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DesignOrderForm
from .forms_deliverable import DeliverableForm
from .models import DesignOrder, DesignPackage
from .models import Deliverable
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

@staff_member_required
def deliverable_upload(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id)

    if request.method == "POST":
        form = DeliverableForm(request.POST, request.FILES)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.order = order
            deliverable.save()

            if order.status in ["paid", "in_progress"]:
                order.status = "delivered"
                order.save()

            messages.success(request, "Deliverable uploaded.")
            return redirect("order_admin_detail", order_id=order.id)
        messages.error(request, "Please fix the errors below.")
    else:
        form = DeliverableForm()

    return render(request, "orders/deliverable_form.html", {"form": form, "order": order})


@staff_member_required
def deliverable_delete(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)
    order_id = deliverable.order.id

    if request.method == "POST":
        deliverable.delete()
        messages.success(request, "Deliverable deleted.")
        return redirect("order_admin_detail", order_id=order_id)

    return render(request, "orders/deliverable_confirm_delete.html", {"deliverable": deliverable})

@staff_member_required
def order_admin_detail(request, order_id):
    order = get_object_or_404(DesignOrder, id=order_id)
    return render(request, "orders/order_admin_detail.html", {"order": order})
