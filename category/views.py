from django.shortcuts import render
from products.models import Product
from slider.models import Slider
from category.models import Category

def home(request):
    category = Category.objects.filter(status=0)
    slides = Slider.objects.filter(is_active=True)

    home_products = Product.objects.filter(
        is_available=True
    ).order_by('-created_date')[:16]   # 👈 latest 16 products

    return render(request, 'home_category.html', {
        'category': category,
        'slides': slides,
        'home_products': home_products
    })
