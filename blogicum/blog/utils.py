from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Post


def get_filter_posts(posts=Post.objects, post_id=None, filter_posts=True):
    posts = (
        posts.select_related(
            'category',
            'location',
            'author',
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    if filter_posts:
        posts = posts.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    if post_id:
        return get_object_or_404(posts, pk=post_id)
    return posts
