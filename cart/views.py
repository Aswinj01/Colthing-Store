from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariation
from .models import Cart, CartItem


# -----------------------------------
# GET OR CREATE CART (SAFE VERSION)
# -----------------------------------
def _get_cart(request):

    # Make sure session exists
    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(
            session_id=request.session.session_key
        )

    return cart


# -----------------------------------
# CART PAGE
# -----------------------------------
def cart_view(request):

    cart = _get_cart(request)
    cart_items = cart.items.all()

    subtotal = sum(item.sub_total() for item in cart_items)

    SHIPPING = 50
    FREE_LIMIT = 1500

    shipping = 0 if subtotal >= FREE_LIMIT or subtotal == 0 else SHIPPING
    grand_total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "total": subtotal,
        "shipping": shipping,
        "grand_total": grand_total,
    }

    return render(request, "products/cart.html", context)


# -----------------------------------
# ADD TO CART
# -----------------------------------
def add_to_cart(request, product_id):

    if request.method != "POST":
        return redirect("home")

    product = get_object_or_404(Product, id=product_id)

    size = request.POST.get("size")
    quantity = int(request.POST.get("quantity", 1))

    if not size:
        messages.error(request, "Please select size")
        return redirect(product.get_url())

    variation = get_object_or_404(
        ProductVariation,
        product=product,
        size=size,
        is_active=True
    )

    cart = _get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size
    )

    new_qty = cart_item.quantity + quantity if not created else quantity

    # Stock validation
    if new_qty > variation.stock:
        messages.error(request, f"Only {variation.stock} items available")
        return redirect(product.get_url())

    cart_item.quantity = new_qty
    cart_item.save()

    messages.success(request, "Item added to cart")

    return redirect("cart")


# -----------------------------------
# REMOVE ITEM
# -----------------------------------
def remove_cart(request, item_id):

    cart = _get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    cart_item.delete()

    messages.success(request, "Item removed from cart")

    return redirect("cart")