from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='name',
                            help_text='name of category')
    slug = models.SlugField(max_length=100, unique=True,
                            default='',
                            verbose_name='slug',
                            help_text='unique slug')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name='name',
                            help_text='name of genre')
    slug = models.SlugField(max_length=100, unique=True,
                            default='',
                            verbose_name='slug',
                            help_text='unique slug')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Title(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name='name',
                            help_text='name of title')
    year = models.IntegerField(default=0,
                               verbose_name='year',
                               help_text='year when title was published')
    category = models.ForeignKey(Category,
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='media',
                                 verbose_name='category',
                                 help_text='category of a title')
    description = models.TextField(default='')
    genre = models.ManyToManyField('Genre',
                                   blank=True,
                                   related_name='media',
                                   verbose_name='genre',
                                   help_text='genres list of a title')

    def __str__(self):
        return f'{self.name} - media of {self.category}'

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    score = models.IntegerField(validators=(
                                MinValueValidator(1),
                                MaxValueValidator(10))
                                )
    text = models.TextField(null=False)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
