from django.db import models
from apps.stores.models import Collection  # Add this import

# Create your models here.
class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    SKU = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    total_sold = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-date_added"]

    def __str__(self):
        return self.name