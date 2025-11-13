from django.contrib import admin
from .models import Order, OrderItem

# Inline so OrderItems appear inside each Order in admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # how many empty slots to show

# Custom Order admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'completed')
    list_filter = ('completed', 'date_ordered')
    inlines = [OrderItemInline]

# Register Order with the custom admin
admin.site.register(Order, OrderAdmin)
