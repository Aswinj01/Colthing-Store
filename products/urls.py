from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path(
        'products/<slug:category_slug>/<slug:product_slug>/',
        views.product_detail,
        name='product_detail'
    ),
]
