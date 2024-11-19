from django.urls import path
from . import views
urlpatterns = [
    path('',views.all_products,name='all_products'),
    path('product_details/',views.product_details,name='product_details'),
    path('add_product/',views.add_product,name='add_product'),
]
