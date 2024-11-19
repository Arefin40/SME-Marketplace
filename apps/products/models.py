from django.db import models
from apps.users.models import User
from apps.stores.models import Collection
from django.core.validators import MinValueValidator, MaxValueValidator


# ===================================
# Product Model
# ===================================
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


# ===================================
# Product Image Model
# ===================================
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    class Meta:
        db_table = "product_images"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


# ===================================
# Review Model
# ===================================
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ("user", "product")
