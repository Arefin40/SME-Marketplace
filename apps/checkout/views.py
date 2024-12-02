from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import CartItem


# Create your views here.
@login_required
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(
        request, "shopping_cart.html", {"cart_items": cart_items, "total_price": total_price}
    )


@login_required
def add_to_cart(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.success(request, "Product added to cart")

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def decrement_quantity(request, pk):
    cart_item = CartItem.objects.get(user=request.user, product=pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    CartItem.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def clear_cart(request):
    user = request.user
    CartItem.objects.filter(user=user).delete()
    return redirect("cart")
