from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .forms import CheckoutForm
from .models import Order, OrderItem


def _get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            session_id = request.session.create()
        cart = Cart.objects.filter(session_id=session_id).first()
    return cart


@login_required
def checkout(request):

    # -----------------------------
    # GET CART (USER OR SESSION)
    # -----------------------------
    cart = _get_cart(request)

    if not cart:
        return redirect('cart')

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart')

    # -----------------------------
    # TOTAL CALCULATION
    # -----------------------------
    total = sum(item.product.offer_price * item.quantity for item in cart_items)
    shipping = 60
    grand_total = total + shipping

    # -----------------------------
    # PLACE ORDER
    # -----------------------------
    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = grand_total
            order.save()

            # CREATE ORDER ITEMS
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.size,   # ✅ ADD THIS
                    price=item.product.offer_price,
                    quantity=item.quantity
                )

            # CLEAR CART
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

@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')