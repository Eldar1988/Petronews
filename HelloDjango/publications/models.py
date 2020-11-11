from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from HelloDjango.settings import path_and_rename
from django.urls import reverse

from profiles.models import Author


class Category(models.Model):
    """Категория"""
    name = models.CharField('Название категории', max_length=200)
    order = models.PositiveSmallIntegerField('Порядок сортировки (необязательно)', blank=True, null=True)
    slug = models.SlugField('Slug', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('publication_category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('order',)


class Publication(models.Model):
    """Публикация"""
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория',
                                 related_name='publications')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор',
                               related_name='authors')
    title = models.CharField('Заголовок', max_length=255, db_index=True)
    image = models.ImageField('Изображение', upload_to=path_and_rename('publications/', 'image'))
    body = RichTextUploadingField('Публикация')
    slug = models.SlugField('Slug', unique=True, help_text='Маленькими буквами, без пробелов и спецсимволов')
    public = models.BooleanField('Опубликовать', default=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    update = models.DateTimeField('Дата обновления', auto_now=True)
    views = models.PositiveSmallIntegerField('Кол-во просмотров', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Review(models.Model):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pub_review')
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пост',
                             related_name='reviews')
    parent = models.ForeignKey('self', verbose_name='Ответ на комментарий', on_delete=models.SET_NULL, null=True,
                               blank=True)
    name = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email')
    public = models.BooleanField('Опубликовать', default=True)
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
