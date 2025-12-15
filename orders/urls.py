from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("new/", views.order_create, name="order_create"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/edit/", views.order_edit, name="order_edit"),
    path("<int:order_id>/delete/", views.order_delete, name="order_delete"),

    # staff obly
    path("admin/<int:order_id>/", views.order_admin_detail, name="order_admin_detail"),
    path("admin/<int:order_id>/deliverables/new/", views.deliverable_upload, name="deliverable_upload"),
    path("admin/deliverables/<int:deliverable_id>/delete/", views.deliverable_delete, name="deliverable_delete"),

]
