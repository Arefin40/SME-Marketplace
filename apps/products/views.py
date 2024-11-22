from django.shortcuts import redirect, render

from apps.products.models import Product


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    return render(request, "all_products.html", {"products": products})


def product_details(request,p_id):
    p = Product.objects.get(pk = p_id)
    return render(request, "product_details.html",{"p":p})


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

            if not all([name, price, stock, sku, image]):
                raise ValueError("Required fields are missing")

            Product.objects.create(
                name=name,
                category=category,
                description=description,
                price=price,
                stock=stock,
                sku=sku,
                image=image,
            )
            return redirect("/")
        except ValueError as v:
            return render(request, "add_product.html", {"error": str(v)})
        except Exception:
            return render(request, "add_product.html", {"error": "An error occurred while saving the product"})
    return render(request, "add_product.html")
