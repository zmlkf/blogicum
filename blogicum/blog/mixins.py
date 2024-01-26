from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment, Post


class CommentMixinView(LoginRequiredMixin):
    """Редактирование или удаление комментария"""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs.get('post_id')
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('post_id')])


class PostMixinView(LoginRequiredMixin):
    """Редактирование или удаление поста"""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs.get(self.pk_url_kwarg)
            )
        return super().dispatch(request, *args, **kwargs)
