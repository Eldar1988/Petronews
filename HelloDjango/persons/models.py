from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from HelloDjango.settings import path_and_rename
from django.urls import reverse


class Person(models.Model):
    """Персона"""
    name = models.CharField('ФИО', max_length=255, db_index=True)
    position = models.CharField('Должность', max_length=255)
    company = models.CharField('Компания', max_length=255)
    image = models.ImageField('Изображение', upload_to=path_and_rename('persons/', 'image'), blank=True,
                              null=True)
    body = RichTextUploadingField('Био')
    slug = models.SlugField('Slug', unique=True, help_text='маленькими буквами, без пробелов и спецсимволов')
    order = models.PositiveSmallIntegerField('Порядковые номер')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('order',)
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

