from django.shortcuts import get_object_or_404, render

from products.models import Product
from .models import *
from slider.models import Slider
from .models import Category
# Create your views here.


def home(request):
    category = Category.objects.filter(status=0)
    slides = Slider.objects.filter(is_active=True)

    return render(request, 'home_category.html', {
        'category': category,
        'slides': slides
    })


