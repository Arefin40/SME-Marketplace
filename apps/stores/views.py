from django.shortcuts import render, redirect
from apps.users.decorators import role_required
from .forms import CreateStoreForm


# Create your views here.
def view_store(request):
    return render(request, "store.html")


def manage_inventory(request):
    return render(request, "manage_inventory.html")


def manage_orders(request):
    return render(request, "manage_orders.html")


@role_required(["MERCHANT"])
def create_store(request):
    if request.method == "POST":
        print(request.POST)
        form = CreateStoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.merchant = request.user
            store.save()
            return redirect("dashboard")
        else:
            print(form.errors)
    else:
        form = CreateStoreForm()
    return render(request, "create_store.html", {"form": form})
