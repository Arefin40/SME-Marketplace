from django.shortcuts import render, redirect
from apps.users.decorators import role_required
from apps.stores.models import Store
from .models import Post


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
