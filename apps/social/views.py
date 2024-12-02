from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.users.decorators import role_required
from apps.stores.models import Store
from apps.products.models import Product
from .models import Post, WishlistItem


# Create your views here.
def get_products(store):
    collections = store.collections.all()
    products = []
    for collection in collections:
        products.extend(collection.products.all())
    return products


@role_required(["MERCHANT"])
def create_post(request):
    store = Store.objects.get(merchant=request.user)
    products = get_products(store)

    if request.method == "POST":
        description = request.POST.get("description")
        selected_product_ids = request.POST.getlist("products")

        post = Post.objects.create(store=store, description=description)

        if selected_product_ids:
            post.products.set(selected_product_ids)
        return redirect("manage-posts")

    return render(request, "post-form.html", {"products": products})


def edit_post(request, pk):
    store = Store.objects.get(merchant=request.user)
    products = get_products(store)
    post = Post.objects.get(pk=pk)

    if request.method == "POST":
        description = request.POST.get("description")
        selected_product_ids = request.POST.getlist("products")

        post.description = description
        post.save()

        if selected_product_ids:
            post.products.set(selected_product_ids)
        return redirect("manage-posts")

    return render(request, "post-form.html", {"post": post, "products": products, "edit": True})


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("manage-posts")


@role_required(["MERCHANT"])
def manage_posts(request):
    store = Store.objects.get(merchant=request.user)
    posts = Post.objects.filter(store=store)
    return render(request, "manage-posts.html", {"posts": posts})


@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def toggle_product_in_wishlist(request, p_id):
    product = Product.objects.get(pk=p_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
    return redirect(request.META.get("HTTP_REFERER"))
