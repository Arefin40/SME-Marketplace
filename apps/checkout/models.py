from django.db import models
from apps.users.models import User
from apps.products.models import Product


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ("user", "product")


class Order(models.Model):
    id = models.CharField(max_length=6, unique=True, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    # Order status
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    # Shipping fields
    shipping_name = models.CharField(max_length=255)
    shipping_contact = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    shipping_zone = models.CharField(max_length=255)
    shipping_area = models.CharField(max_length=255)

    # Billing fields
    billing_name = models.CharField(max_length=255)
    billing_contact = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    billing_zone = models.CharField(max_length=255)
    billing_area = models.CharField(max_length=255)

    # Shipping method
    SHIPPING_CHOICES = [("STANDARD", "Standard Delivery"), ("EXPRESS", "Express Delivery")]
    shipping_method = models.CharField(max_length=10, choices=SHIPPING_CHOICES, default="STANDARD")

    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-order_date"]

    def save(self, *args, **kwargs):
        # Generate order ID like #S12345
        if not self.id:
            last_order = Order.objects.order_by("-id").first()
            if last_order:
                last_number = int(last_order.id[2:])  # Skip 'S' and '#'
                self.id = f"#S{str(last_number + 1).zfill(5)}"
            else:
                self.id = "#S12345"

        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.order.id} - {self.amount}"

    class Meta:
        db_table = "payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
