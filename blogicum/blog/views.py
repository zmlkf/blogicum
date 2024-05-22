from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm
from .mixins import CommentMixinView, PostMixinView
from .models import Category, Post, User
from .utils import get_filtered_posts

DEFAULT_PAGE_SIZE = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostDetailView(DetailView):
    """Page of the requested post"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return get_filtered_posts(
            need_filter=get_object_or_404(
                self.model,
                pk=self.kwargs.get(self.pk_url_kwarg)
            ).author != self.request.user
        )

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': CommentForm(),
            'comments': self.object.comments.select_related('author')
        }


class PostUpdateView(PostMixinView, UpdateView):
    """Edit a post"""

    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])


class PostDeleteView(PostMixinView, DeleteView):
    """Delete a post"""

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'form': PostForm(instance=self.object)
        }

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostListView(ListView):
    """List of posts on the main page"""

    model = Post
    template_name = 'blog/index.html'
    queryset = get_filtered_posts()
    paginate_by = DEFAULT_PAGE_SIZE


class CategoryPostListView(PostListView):
    """List of posts in the requested category"""

    template_name = 'blog/category.html'

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published=True
        )

    def get_queryset(self):
        return get_filtered_posts(posts=self.get_category().posts.all())

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'category': self.get_category()
        }


class UserListView(PostListView):
    """User profile with a list of their posts"""

    template_name = "blog/profile.html"

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )

    def get_queryset(self):
        return get_filtered_posts(
            posts=self.get_author().posts,
            need_filter=self.get_author() != self.request.user
        )

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'profile': self.get_author()
        }


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit profile"""

    model = User
    fields = ('first_name', 'last_name', 'username', 'email')
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.username])


@login_required
def add_comment(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post_obj
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(CommentMixinView, UpdateView):
    """Edit a comment"""

    form_class = CommentForm


class CommentDeleteView(CommentMixinView, DeleteView):
    """Delete a comment"""

    pass
