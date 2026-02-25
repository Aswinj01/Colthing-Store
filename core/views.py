from django.shortcuts import render

def contact_us(request):
    return render(request, "policies/contact.html")

def terms(request):
    return render(request, "policies/terms.html")

def refund_policy(request):
    return render(request, "policies/refund.html")