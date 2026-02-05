from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product, ProductVariation
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")

    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get("size")
    quantity = int(request.POST.get("quantity", 1))

    if not size:
        messages.error(request, "Please select a size!")
        return redirect(product.get_url())

    variation = get_object_or_404(
        ProductVariation,
        product=product,
        size=size,
        is_active=True
    )

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size
    )

    # 👉 TOTAL quantity user wants
    new_qty = cart_item.quantity + quantity if not created else quantity

    # ❌ Block if exceeds stock
    if new_qty > variation.stock:
        messages.error(
            request,
            f"Only {variation.stock} item(s) available for size {size}"
        )
        return redirect(product.get_url())

    cart_item.quantity = new_qty
    cart_item.save()

    messages.success(request, f"{product.product_name} ({size}) added to cart!")
    return redirect("cart")


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = sum(item.sub_total() for item in cart_items)

    # SHIPPING RULE
    SHIPPING_CHARGE = 50
    FREE_SHIPPING_LIMIT = 1500

    if subtotal >= FREE_SHIPPING_LIMIT or subtotal == 0:
        shipping = 0
    else:
        shipping = SHIPPING_CHARGE

    grand_total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "total": subtotal,
        "shipping": shipping,
        "grand_total": grand_total,
    }
    return render(request, "products/cart.html", context)



@login_required
def remove_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart")
