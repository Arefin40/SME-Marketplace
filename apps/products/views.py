import markdown
from django.contrib import messages
from django.shortcuts import redirect, render
from apps.users.decorators import role_required
from apps.stores.models import Collection
from .models import Product, ProductImage
from .forms import ProductForm


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    return render(request, "all_products.html", {"products": products})


def product_details(request, p_id):
    p = Product.objects.get(pk=p_id)
    p.description = markdown.markdown(
        convert_to_markdown_table(p.description), extensions=["markdown.extensions.tables"]
    )
    return render(request, "product_details.html", {"p": p})


def add_product(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            category = request.POST.get("category")
            description = request.POST.get("description")
            price = request.POST.get("price")
            stock = request.POST.get("stock")
            sku = request.POST.get("sku")
            image = request.FILES.get("image")



def convert_to_markdown_table(textarea_input):
    rows = textarea_input.strip().split("\n")
    table = "| Feature | Description |\n| -- | -- |\n"

    for row in rows:
        if ":" in row:
            key, values = row.split(":", 1)
            values = values.strip().replace("|", "<br>")
            table += f"| **{key.strip()}** | {values} |\n"
    return table
