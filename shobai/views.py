import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from apps.social.models import Post, PostLike
from apps.stores.models import Store, StoreFollow


@login_required
def homepage(request):
    """View function for the homepage"""
    posts = Post.objects.annotate(
        user_has_liked=models.Exists(
            PostLike.objects.filter(post=models.OuterRef("pk"), user=request.user)
        )
    ).all()

    for post in posts:
        post.description = markdown.markdown(post.description)

    stores = Store.objects.annotate(
        is_following=models.Exists(
            StoreFollow.objects.filter(store=models.OuterRef("pk"), user=request.user)
        )
    ).all()

    return render(request, "homepage.html", {"posts": posts, "stores": stores})


@login_required
def dashboard(request):
    """View function for the dashboard"""
    return render(request, "dashboard.html")
