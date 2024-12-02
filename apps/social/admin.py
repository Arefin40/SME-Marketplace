from django.contrib import admin
from .models import Post, PostLike, WishlistItem

# Register your models here.
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(WishlistItem)
