from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .forms import CheckoutForm
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 60
    grand_total = total + shipping

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = grand_total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            cart_items.delete()
            return redirect('order_success')

    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'shipping': shipping,
        'grand_total': grand_total
    })
