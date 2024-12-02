import markdown
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from apps.users.decorators import role_required
from apps.stores.models import Collection
from .models import Product, ProductImage
from .forms import ProductForm


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    wishlist_products = request.user.wishlist_items.values_list("product_id", flat=True)

    # Handle search query
    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    return render(
        request, "all_products.html", {"products": products, "wishlist_products": wishlist_products}
    )


def product_details(request, p_id):
    p = Product.objects.get(pk=p_id)
    p.description = markdown.markdown(
        convert_to_markdown_table(p.description), extensions=["markdown.extensions.tables"]
    )
    return render(request, "product_details.html", {"p": p})


@role_required(["MERCHANT"])
def add_product(request):
    if not request.user.stores.exists():
        messages.error(request, "You need to create a store first before adding products.")
        return redirect("create-store")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = request.user.stores.first()

            # Create new collection if specified
            collection = form.cleaned_data.get("collection")
            new_collection_name = form.cleaned_data.get("new_collection_name")

            if not collection and new_collection_name:
                product.collection = Collection.objects.create(
                    name=new_collection_name, store=product.store
                )
            else:
                product.collection = collection

            product.save()

            # Save additional product images
            for image in request.FILES.getlist("images"):
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Product added successfully!")
            return redirect("manage-inventory")
    else:
        form = ProductForm(user=request.user)

    return render(request, "product_form.html", {"form": form})


@role_required(["MERCHANT"])
def update_product(request, p_id):
    p = Product.objects.get(pk=p_id)

    if request.user != p.collection.store.merchant:
        raise PermissionDenied

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=p, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("manage-inventory")

    form = ProductForm(instance=p, user=request.user)
    return render(request, "product_form.html", {"form": form, "update": True})


def convert_to_markdown_table(textarea_input):
    rows = textarea_input.strip().split("\n")
    table = "| Feature | Description |\n| -- | -- |\n"

    for row in rows:
        if ":" in row:
            key, values = row.split(":", 1)
            values = values.strip().replace("|", "<br>")
            table += f"| **{key.strip()}** | {values} |\n"
    return table
