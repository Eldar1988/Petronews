from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from HelloDjango.settings import path_and_rename
from django.urls import reverse


class Category(models.Model):
    """Категория"""
    name = models.CharField('Название категории', max_length=200)
    order = models.PositiveSmallIntegerField('Порядок сортировки (необязательно)', blank=True, null=True)
    slug = models.SlugField('Slug', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('order',)


class Post(models.Model):
    """ Новость"""
    parse_category = models.CharField('Категория(parse)', blank=True, null=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='news',
                                 null=True, blank=True)
    parse_title = models.CharField('Заголовок (parse)', max_length=255, db_index=True, blank=True, null=True)
    title = models.CharField('Заголовок', max_length=555, db_index=True)
    kz_news = models.BooleanField('Каз', default=False)
    world_news = models.BooleanField('Мир', default=False)
    main_news = models.BooleanField('Главное', default=False)
    is_actual = models.BooleanField('Актуальное', default=False)
    public = models.BooleanField('Опубликовать', default=False)
    image_url = models.URLField('Ссылка на изображение(parsed)', blank=True, null=True)
    image = models.ImageField('Изображение (необязательно)', upload_to=path_and_rename('news/', 'image'), blank=True,
                              null=True)
    body = RichTextUploadingField('Новость', blank=True, null=True)
    views = models.PositiveSmallIntegerField('Количество просмотров', default=0)
    source = models.URLField('Источник новости', blank=True, null=True)
    main_source = models.CharField('Источник', blank=True, null=True, max_length=255)
    pub_date = models.DateTimeField('Опубликовано', auto_now_add=True)
    update_date = models.DateTimeField('Обновлено', auto_now=True)
    slug = models.SlugField('Slug', unique=True, null=True, blank=True)
    telegram_send = models.BooleanField('Опубликовано в телеграме', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-pub_date', 'update_date')


class PostForCompare(models.Model):
    """Модель для сравнения уже загруженных новостей"""
    title = models.CharField(max_length=555)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_review')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пост',
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


class Notification(models.Model):
    """Отчеты и уведомления"""
    not_text = models.TextField('Уведомление')
    pub_date = models.DateTimeField('Время и дата', auto_now_add=True)

    def __str__(self):
        return self.not_text

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('pub_date',)
