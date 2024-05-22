from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Not set'


class CommentAdmin(admin.TabularInline):

    model = Comment
    readonly_fields = ('text', 'author', 'created_at')
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentAdmin,
    ]

    list_display = (
        'title',
        'short_text_field',
        'comment_count',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'post_image'
    )

    @admin.display(description='Text')
    def short_text_field(self, post):
        return post.text[:50]

    @admin.display(description='Comments')
    def comment_count(self, obj):
        return obj.comments.count()

    @admin.display(description='Image')
    def post_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50')

    list_editable = (
        'is_published',
        'category'
    )

    search_fields = ('title',)
    list_filter = ('category',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'short_description_field',
        'slug',
        'is_published'
    )

    @admin.display(description='Description')
    def short_description_field(self, description):
        # Limiting the number of characters in the text
        return description.description[:50]

    list_editable = ('is_published',)
