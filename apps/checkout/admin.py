from django.contrib import admin
from .models import CartItem, Order, Payment

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Payment)
