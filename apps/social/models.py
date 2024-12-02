from django.db import models
from apps.stores.models import Store
from apps.products.models import Product
from apps.users.models import User


# Create your models here.
class Post(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    products = models.ManyToManyField(Product, related_name="posts")
    total_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store.name} - {self.description[:10]}..."

    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} liked {self.post.description[:10]}..."

    class Meta:
        db_table = "post_likes"
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"
        ordering = ["-created_at"]


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"

    class Meta:
        db_table = "wishlist_items"
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        ordering = ["-created_at"]
