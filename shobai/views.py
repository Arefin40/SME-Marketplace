import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.social.models import Post, PostLike
from apps.stores.models import Store, StoreFollow
from apps.checkout.models import Order, OrderItem
from apps.products.models import Product


@login_required
def homepage(request):
    """View function for the homepage"""
    posts = Post.objects.annotate(
        user_has_liked=models.Exists(
            PostLike.objects.filter(post=models.OuterRef("pk"), user=request.user)
        )
    ).all()

    for post in posts:
        post.description = markdown.markdown(post.description)

    stores = Store.objects.annotate(
        is_following=models.Exists(
            StoreFollow.objects.filter(store=models.OuterRef("pk"), user=request.user)
        )
    ).all()

    return render(request, "homepage.html", {"posts": posts, "stores": stores})


@login_required
def dashboard(request):
    if request.user.role == "ADMIN":
        total_users = User.objects.count()
        total_stores = Store.objects.count()
        total_orders = Order.objects.count()

        recent_orders = Order.objects.all().order_by("-order_date")[:5]

        return render(
            request,
            "dashboard_admin.html",
            {
                "total_users": total_users,
                "total_stores": total_stores,
                "total_orders": total_orders,
                "orders": recent_orders,
            },
        )
    elif request.user.role == "MERCHANT":
        today = timezone.now().date()
        store = Store.objects.get(merchant=request.user)

        # Get orders that contain products from this store
        store_orders = Order.objects.filter(
            items__product__collection__store=store, order_date__date=today
        ).distinct()

        total_orders = store_orders.count()

        total_revenue = store_orders.aggregate(total=models.Sum("total_price"))["total"] or 0

        total_products = Product.objects.filter(collection__store=store).count()

        recent_orders = (
            Order.objects.filter(items__product__collection__store=store)
            .distinct()
            .order_by("-order_date")[:5]
        )

        return render(
            request,
            "dashboard_store.html",
            {
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "total_products": total_products,
                "orders": recent_orders,
            },
        )
    return render(request, "dashboard.html")
