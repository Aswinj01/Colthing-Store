from .models import Cart, CartItem

# cart/context_processors.py
def cart_count(request):
    if request.user.is_authenticated:
        from .models import CartItem
        count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}
