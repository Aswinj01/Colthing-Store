from django.contrib import admin
from .models import Product, ProductVariation

# Inline for variations (sizes + stock)
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1  # How many blank rows to show
    min_num = 1
    max_num = 10
    # optional: readonly_fields = ('stock',)

# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'original_price', 'offer_price', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductVariationInline]  # <-- THIS LINE IS THE KEY

# Register product with inline
admin.site.register(Product, ProductAdmin)
