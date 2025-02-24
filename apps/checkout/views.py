from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.decorators import role_required
from apps.products.models import Product
from .models import CartItem, Order, OrderItem
from .forms import CheckoutForm


# Create your views here.
@login_required
def cart(request):
    user = request.user
    cart_items, total_price = get_cart_items_and_total_price(user)
    return render(
        request, "shopping_cart.html", {"cart_items": cart_items, "total_price": total_price}
    )


@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user
    if product.collection.store.merchant == user:
        messages.error(request, "You are not allowed to add this product to cart")
        return redirect(request.META.get("HTTP_REFERER"))

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


@login_required
def checkout(request):
    user = request.user
    addresses = user.addresses.all()
    cart_items, total_price = get_cart_items_and_total_price(user)

    form = CheckoutForm()
    return render(
        request,
        "checkout.html",
        {
            "addresses": addresses,
            "form": form,
            "total_price": total_price,
            "shipping_price": 60,
            "grand_total": total_price + 60,
        },
    )


@login_required
def place_order(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart_items, total_price = get_cart_items_and_total_price(request.user)
            cleaned_data = form.cleaned_data.copy()

            # Convert Zone to string value for CharField
            cleaned_data["shipping_zone"] = str(cleaned_data["shipping_zone"])
            cleaned_data["billing_zone"] = str(cleaned_data["billing_zone"])
            # Convert Area to string value for CharField
            cleaned_data["shipping_area"] = str(cleaned_data["shipping_area"].name)
            cleaned_data["billing_area"] = str(cleaned_data["billing_area"].name)

            order = Order.objects.create(user=request.user, **cleaned_data, total_price=total_price)

            # Transfer cart items to order items
            for i in cart_items:
                OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity)

            # Clear cart items
            cart_items.delete()

            return redirect("thankyou", order_id=order.id)

    return redirect("checkout")


@login_required
def thankyou(request, order_id):
    if not order_id:
        return redirect("home")

    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, "thankyou.html", {"order": order, "order_items": order_items})


def get_cart_items_and_total_price(user):
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return cart_items, total_price


@role_required(["ADMIN", "MERCHANT"])
def received_orders(request):
    if request.user.role == "ADMIN":
        # Admin sees all orders
        orders = Order.objects.all().order_by("-order_date")
        return render(request, "manage_orders.html", {"orders": orders})

    elif request.user.role == "MERCHANT":
        merchant_orders = (
            Order.objects.filter(
                items__product__collection__store__merchant=request.user, status="PENDING"
            )
            .distinct()
            .order_by("-order_date")
        )
        return render(request, "received_orders.html", {"orders": merchant_orders})

    return redirect("home")


@login_required
def orders_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-order_date")
    return render(request, "orders_history.html", {"orders": orders})


@login_required
def order_details(request, pk):
    order = Order.objects.get(id=pk)

    if request.user.role == "MERCHANT":
        order_items = OrderItem.objects.filter(
            order=order, product__collection__store__merchant=request.user
        )
    else:
        order_items = OrderItem.objects.filter(order=order)

    return render(
        request,
        "order_details_admin.html" if request.user.role == "ADMIN" else "order_details.html",
        {"order": order, "order_items": order_items},
    )
