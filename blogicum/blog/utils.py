from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_filter_posts(posts=Post.objects, need_filter=True):
    posts = (
        posts.select_related(
            'category',
            'location',
            'author',
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    if need_filter:
        posts = posts.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    return posts
