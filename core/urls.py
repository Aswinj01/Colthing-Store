from django.urls import path
from . import views

urlpatterns = [
    path("contact-us/", views.contact_us, name="contact_us"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("refund-policy/", views.refund_policy, name="refund_policy"),
]