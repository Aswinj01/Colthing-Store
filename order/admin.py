from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


# 🔹 Inline for Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product',
        'product_image',
        'size',
        'price',
        'quantity',
    )

    def product_image(self, obj):
        if obj.product.main_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="60" height="60" style="border-radius:8px;" />'
                '</a>',
                obj.product.main_image.url,
                obj.product.main_image.url
            )
        return "No Image"

    product_image.short_description = "Image"


# 🔹 Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_id',
        'customer_name',
        'phone',
        'city',
        'total_price',
        'created_at',
    )

    search_fields = (
        'order_id',
        'first_name',
        'last_name',
        'phone',
        'email',
    )

    ordering = ('-created_at',)

    readonly_fields = ('order_id', 'created_at')

    inlines = [OrderItemInline]

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    customer_name.short_description = "Customer Name"