from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.users.decorators import role_required
from .forms import CreateStoreForm
from .models import Store, StoreFollow


# Create your views here.
@login_required
def store(request, slug):
    try:
        store = Store.objects.get(slug=slug)
        collections = store.collections.all().prefetch_related("products")
        is_following = StoreFollow.objects.filter(user=request.user, store=store).exists()
        return render(
            request,
            "store.html",
            {"store": store, "collections": collections, "is_following": is_following},
        )
    except Store.DoesNotExist:
        return redirect(request.META.get("HTTP_REFERER", "home"))


@role_required(["MERCHANT"])
def manage_inventory(request):
    store = Store.objects.filter(merchant=request.user).first()
    collections = store.collections.all().prefetch_related("products") if store else []
    products = []
    for collection in collections:
        products.extend(collection.products.all())

    # Handle search query
    query = request.GET.get("q")
    if query:
        filtered_products = []
        for product in products:
            if query.lower() in product.name.lower() or query.lower() in product.sku.lower():
                filtered_products.append(product)
        products = filtered_products

    return render(request, "manage_inventory.html", {"products": products})


def manage_orders(request):
    return render(request, "manage_orders.html")


@role_required(["MERCHANT"])
def create_store(request):
    if request.method == "POST":
        form = CreateStoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.merchant = request.user
            store.save()
            return redirect("dashboard")
    else:
        form = CreateStoreForm()
    return render(request, "create_store.html", {"form": form})


@role_required(["USER", "MERCHANT"], redirect_url="CURRENT")
def toggle_follow_store(request, slug):
    try:
        store = Store.objects.get(slug=slug)
        if store.merchant != request.user:
            follow, created = StoreFollow.objects.get_or_create(user=request.user, store=store)
            if not created:
                follow.delete()
    except Store.DoesNotExist:
        pass

    return redirect(request.META.get("HTTP_REFERER"))
