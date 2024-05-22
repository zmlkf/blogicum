from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PublishedModel(models.Model):
    """Abstract model.
    Adds the is_published flag and the publication creation date and time
    """

    is_published = models.BooleanField(
        'Published',
        default=True,
        help_text='Uncheck to hide the publication.'
    )
    created_at = models.DateTimeField('Added', auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField('Title', max_length=256)
    description = models.TextField('Description')
    slug = models.SlugField(
        'Identifier',
        max_length=256,
        unique=True,
        help_text=('Page identifier for the URL; '
                   'allowing characters: '
                   'Latin letters, numbers, hyphens, and underscores.')
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title[:20]


class Location(PublishedModel):
    name = models.CharField('Location Name', max_length=256)

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name[:20]


class Post(PublishedModel):
    title = models.CharField('Title', max_length=256)
    text = models.TextField('Text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Publication Author'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Location'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Category'
    )
    image = models.ImageField(
        'Image',
        upload_to='post_images',
        blank=True
    )
    pub_date = models.DateTimeField(
        'Publication Date and Time',
        help_text=('If you set a date and time '
                   'in the future, you can schedule posts.')
    )

    class Meta:
        verbose_name = 'publication'
        verbose_name_plural = 'Publications'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:50]


class Comment(models.Model):
    text = models.TextField('Comment')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Post'
    )
    created_at = models.DateTimeField(
        'Added',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'
        ordering = ('created_at',)
        default_related_name = 'comments'

    def __str__(self):
        return f'Comment by user {self.author} '
