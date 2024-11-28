from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver
from apps.users.models import User


# ===================================
# Store Model
# ===================================
class Store(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(
        upload_to="stores/logos/", default="stores/logos/default.svg", blank=True, null=True
    )
    cover = models.ImageField(
        upload_to="stores/covers/", default="stores/covers/default.svg", blank=True, null=True
    )
    description = models.TextField()
    followers = models.ManyToManyField(
        User, through="StoreFollow", related_name="followed_stores", blank=True
    )
    total_followers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "stores"
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - @{self.slug}"


# ===================================
# Store Follow Model
# ===================================
class StoreFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_follows"
        verbose_name = "Store Follow"
        verbose_name_plural = "Store Follows"
        unique_together = ["user", "store"]

    def __str__(self):
        return f"{self.user.name} - {self.store.name}"


@receiver(post_save, sender=StoreFollow)
def increment_total_followers(sender, instance, created, **kwargs):
    if created:
        instance.store.total_followers += 1
        instance.store.save(update_fields=["total_followers"])


@receiver(post_delete, sender=StoreFollow)
def decrement_total_followers(sender, instance, **kwargs):
    if instance.store.total_followers > 0:
        instance.store.total_followers -= 1
        instance.store.save(update_fields=["total_followers"])


# ===================================
# Collection Model
# ===================================
class Collection(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="collections/covers/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collections"
        verbose_name = "Store Collection"
        verbose_name_plural = "Store Collections"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.store.name} - {self.name}"
