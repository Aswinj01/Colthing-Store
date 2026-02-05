from django.urls import path
from category import views

urlpatterns = [
    path('', views.home, name="home"),
    path("category/<slug:slug>/", views.Category, name="category_products"),
]
