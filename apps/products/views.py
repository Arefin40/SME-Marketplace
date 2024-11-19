from django.shortcuts import render


# Create your views here.
def all_products(request):
    return render(request, "all_products.html")


def product_details(request):
    return render(request, "product_details.html")


def add_product(request):
    return render(request, "add_product.html")
