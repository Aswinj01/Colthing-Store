from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404

from category.models import Category
from .models import Product, ProductVariation


def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    # Attach stock from ProductVariation
    for product in products:
        variation = ProductVariation.objects.filter(
            product=product,
            is_active=True
        ).first()

        product.stock = variation.stock if variation else 0

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'products/product_list.html', context)



def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True
    )

    # Get ALL sizes (even stock = 0)
    sizes = ProductVariation.objects.filter(
        product=product,
        is_active=True
    )

    # Check if ANY size has stock
    in_stock = sizes.filter(stock__gt=0).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'sizes': sizes,
        'in_stock': in_stock
    })
