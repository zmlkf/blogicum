from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm
from .mixins import CommentMixinView, PostMixinView
from .models import Category, Post, User
from .utils import get_filter_posts

DEFAULT_PAGE_SIZE = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostDetailView(DetailView):
    """Страница запрашиваемого поста"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post_obj = get_object_or_404(
            self.model,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )
        if post_obj.author != self.request.user:
            post_obj = get_filter_posts(
                self.model.objects,
                self.kwargs.get(self.pk_url_kwarg),
            )
        return post_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(
            context,
            form=CommentForm(),
            comments=self.object.comments.select_related('author')
        )


class PostUpdateView(PostMixinView, UpdateView):
    """Редактирование поста"""

    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])


class PostDeleteView(PostMixinView, DeleteView):
    """Удаление поста"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(context, form=PostForm(instance=self.object))

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostListView(ListView):
    """Список постов на главной странице"""

    model = Post
    template_name = 'blog/index.html'
    queryset = get_filter_posts()
    paginate_by = DEFAULT_PAGE_SIZE


class CategoryPostListView(PostListView):
    """Список постов в запрошенной категории"""

    template_name = 'blog/category.html'

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published=True
        )

    def get_queryset(self):
        return get_filter_posts(self.get_category().posts.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(context, category=self.get_category())


class UserListView(PostListView):
    """Профиль пользоателя со списком его постов"""

    template_name = "blog/profile.html"

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )

    def get_queryset(self):
        return get_filter_posts(
            self.get_author().posts,
            filter_posts=self.get_author() != self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(context, profile=self.get_author())


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""

    model = User
    fields = ('first_name', 'last_name', 'username', 'email')
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.username])


@login_required
def add_comment(request, post_id):
    post_obj = get_filter_posts(post_id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post_obj
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentUpdateView(CommentMixinView, UpdateView):
    """Редактирование комментария"""

    form_class = CommentForm


class CommentDeleteView(CommentMixinView, DeleteView):
    """Удаление комментария"""

    pass
